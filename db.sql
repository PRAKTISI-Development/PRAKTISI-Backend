-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 06 Feb 2024 pada 17.45
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `praktisi_new`
--

DELIMITER $$
--
-- Prosedur
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `akumulasi_nilai_dan_kehadiran` (IN `matkul_code` VARCHAR(255))   BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE tugas_count INT;

    -- HITUNG JUMLAH TUGAS
    SELECT COUNT(DISTINCT kd_tugas) INTO tugas_count 
    FROM tugas 
    INNER JOIN matkul_prak ON tugas.kd_matkul = matkul_prak.kd_matkul 
    WHERE matkul_prak.kd_matkul = matkul_code;

    -- THE QUERIES
    CREATE TEMPORARY TABLE IF NOT EXISTS PraktikanCTE (
        NIM CHAR(10),
        kd_matkul CHAR(10),
        kd_tugas CHAR(10),
        nama_lengkap VARCHAR(255),
        semester VARCHAR(30),
        praktikum VARCHAR(255),
        nilai_tugas INT,
        nilai_akhir INT,
        jenis_tugas VARCHAR(255),
        row_num INT,
        akumulasi_posttest DECIMAL(10, 2)
    );

INSERT INTO PraktikanCTE
SELECT
    users.userid AS NIM,
    matkul_prak.kd_matkul,
    tugas.kd_tugas AS kd_tugas,
    users.nama AS nama_lengkap,
    users.semester AS semester,
    matkul_prak.nama_matkul AS praktikum,
    COALESCE(detail_pengumpulan.nilai_tugas, 0) AS nilai_tugas,
    nilai_akhir.nilai_akhir AS nilai_akhir,
    tugas.jenis_tugas,
    ROW_NUMBER() OVER (PARTITION BY users.userid, matkul_prak.kd_matkul ORDER BY detail_pengumpulan.nilai_tugas) AS row_num,
    0 AS akumulasi_posttest -- Nilai awal untuk kolom akumulasi_posttest
FROM users 
    LEFT JOIN detail_pengumpulan ON users.userid = detail_pengumpulan.usersid
    INNER JOIN nilai_akhir ON users.userid = nilai_akhir.usersid
    INNER JOIN matkul_prak ON nilai_akhir.kd_matkul = matkul_prak.kd_matkul
    LEFT JOIN tugas ON tugas.kd_matkul = matkul_prak.kd_matkul 
        AND detail_pengumpulan.kd_tugas = tugas.kd_tugas -- Tambahkan kondisi ini
WHERE users.praktikan = 1
    AND matkul_prak.kd_matkul = matkul_code;


-- Inisialisasi variabel untuk akumulasi posttest
SET @posttest_sum := 0;
SET @posttest_count := 0;

-- Dynamic column list for posttest
SET @posttest_columns := '';
SET i = 1;
WHILE i <= tugas_count DO
    IF EXISTS (
        SELECT 1 FROM tugas 
        WHERE tugas.kd_matkul = (SELECT kd_matkul FROM matkul_prak WHERE kd_matkul = matkul_code) 
        AND jenis_tugas = 'Post Test' 
        AND i <= tugas_count
    ) THEN
        SET @posttest_columns := CONCAT(@posttest_columns, ', COALESCE(MAX(CASE WHEN row_num = ', i, ' AND PraktikanCTE.jenis_tugas = ''Post Test'' THEN nilai_tugas END),0) AS posttest_', i);
    END IF;
    SET i = i + 1;
END WHILE;

-- Inisialisasi tabel sementara untuk menyimpan hasil akumulasi posttest
CREATE TEMPORARY TABLE IF NOT EXISTS TugasAccumulation (
    NIM CHAR(10),
    kd_matkul VARCHAR(255),
    posttest_sum DECIMAL(10,2),
    posttest_count INT
);

-- Hitung nilai akumulasi posttest untuk setiap NIM dan kd_matkul
INSERT INTO TugasAccumulation (NIM, kd_matkul, posttest_sum, posttest_count)
SELECT 
    NIM, 
    kd_matkul, 
    SUM(nilai_tugas), 
    COUNT(nilai_tugas)
FROM PraktikanCTE
WHERE jenis_tugas = 'Post Test'
GROUP BY NIM, kd_matkul;

-- Perbarui kolom akumulasi_posttest dalam tabel PraktikanCTE
UPDATE PraktikanCTE
JOIN TugasAccumulation ON PraktikanCTE.NIM = TugasAccumulation.NIM AND PraktikanCTE.kd_matkul = TugasAccumulation.kd_matkul
SET PraktikanCTE.akumulasi_posttest = TugasAccumulation.posttest_sum / TugasAccumulation.posttest_count;

-- Hapus tabel sementara setelah digunakan
DROP TEMPORARY TABLE IF EXISTS TugasAccumulation;

    -- THE SELECT QUERY
    SET @sql_query_select := CONCAT('
        SELECT
            NIM,
            nama_lengkap,
            semester,
            praktikum,
            COALESCE((SELECT COUNT(*) * 1.25 FROM kehadiran k INNER JOIN jadwal j ON k.kd_jadwal = j.kd_jadwal
            INNER JOIN matkul_prak m ON m.kd_matkul = j.kd_matkul 
            WHERE m.kd_matkul = ''', matkul_code, ''' AND k.status= ''Hadir'' AND k.usersid = PraktikanCTE.NIM), 0) AS kehadiran',
            @posttest_columns,
            ',
            ROUND(COALESCE(akumulasi_posttest, 0) * 0.4, 2) AS akumulasi_posttest,
            COALESCE(MAX(CASE WHEN jenis_tugas = ''Proyek Akhir'' THEN nilai_tugas END), 0) AS proyek_akhir,
            COALESCE((SELECT COUNT(*) * 1.25 FROM kehadiran k INNER JOIN jadwal j ON k.kd_jadwal = j.kd_jadwal
            INNER JOIN matkul_prak m ON m.kd_matkul = j.kd_matkul 
            WHERE m.kd_matkul = ''', matkul_code, ''' AND k.status= ''Hadir'' AND k.usersid = PraktikanCTE.NIM), 0) + 
            ROUND(COALESCE(akumulasi_posttest, 0) * 0.4, 2) + COALESCE(MAX(CASE WHEN PraktikanCTE.jenis_tugas = ''Proyek Akhir'' THEN nilai_tugas END * 0.6), 0) AS nilai_akhir
        FROM PraktikanCTE
        GROUP BY NIM, nama_lengkap, semester, praktikum;
    ');

    -- RUNNING THE SELECT QUERY
    PREPARE stmt_select FROM @sql_query_select;
    EXECUTE stmt_select;
    DEALLOCATE PREPARE stmt_select;


    -- THE UPDATE QUERY
    SET @sql_query_update := CONCAT('
        UPDATE nilai_akhir
        SET nilai_akhir = (
            SELECT
                ROUND(COALESCE((SELECT COUNT(*) * 1.25 FROM kehadiran k INNER JOIN jadwal j ON k.kd_jadwal = j.kd_jadwal
                INNER JOIN matkul_prak m ON m.kd_matkul = j.kd_matkul 
                WHERE m.kd_matkul = ''', matkul_code, ''' AND k.status= ''Hadir'' AND k.usersid = PraktikanCTE.NIM), 0) + COALESCE(akumulasi_posttest, 0) * 0.4, 2) +
                COALESCE(MAX(CASE WHEN jenis_tugas = ''Proyek Akhir'' THEN nilai_tugas END) * 0.6, 0)
            FROM PraktikanCTE
            WHERE nilai_akhir.kd_matkul = (SELECT kd_matkul FROM matkul_prak WHERE kd_matkul = ''', matkul_code, ''')
            AND nilai_akhir.usersid = PraktikanCTE.NIM
            GROUP BY NIM, nama_lengkap, semester, praktikum
        )
        WHERE nilai_akhir.kd_matkul = (SELECT kd_matkul FROM matkul_prak WHERE kd_matkul = ''', matkul_code, ''');
    ');

    -- RUNNING THE UPDATE QUERY
    PREPARE stmt_update FROM @sql_query_update;
    EXECUTE stmt_update;
    DEALLOCATE PREPARE stmt_update;

    -- Drop temporary table after use
    DROP TEMPORARY TABLE IF EXISTS PraktikanCTE;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `detail_praktikan` (IN `nomor_induk_mhs` CHAR(10))   BEGIN
    WITH data_praktikan AS (
        SELECT
            users.userid AS NIM,
            users.nama AS nama_lengkap,
            matkul_prak.nama_matkul AS praktikum,
            CASE
                WHEN users.asisten_laboratorium = 1 THEN 'Ya' ELSE 'Bukan'
            END AS aslab
        FROM users
            INNER JOIN nilai_akhir ON users.userid = nilai_akhir.usersid
            INNER JOIN matkul_prak ON matkul_prak.kd_matkul = nilai_akhir.kd_matkul
        WHERE
            users.praktikan = 1
            AND users.userid = nomor_induk_mhs
    )
    SELECT * FROM data_praktikan
    ORDER BY NIM ASC, praktikum ASC;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `jadwal` ()   BEGIN
    WITH lihat_jadwal AS (
        SELECT 
            matkul_prak.nama_matkul AS praktikum,
            jadwal.kelas AS kelas,
            jadwal.tanggal AS tanggal,
            jadwal.ruangan AS ruangan,
            jadwal.`waktu_mulai` AS jam_mulai,
            jadwal.`waktu_selesai` AS jam_selesai
        FROM `matkul_prak`
            INNER JOIN jadwal ON matkul_prak.`kd_matkul` = jadwal.`kd_matkul`
    )
    SELECT * FROM lihat_jadwal
    ORDER BY jam_mulai ASC;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Struktur dari tabel `detail_pengumpulan`
--

CREATE TABLE `detail_pengumpulan` (
  `id` int(11) NOT NULL,
  `usersid` char(20) NOT NULL,
  `kd_tugas` char(10) NOT NULL,
  `tanggal_dikumpul` datetime NOT NULL,
  `link_tugas` text DEFAULT NULL,
  `nilai_tugas` int(11) NOT NULL,
  `file_path` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `detail_pengumpulan`
--

INSERT INTO `detail_pengumpulan` (`id`, `usersid`, `kd_tugas`, `tanggal_dikumpul`, `link_tugas`, `nilai_tugas`, `file_path`) VALUES
(1, '2209116004', 'qwertyuiop', '2024-01-11 16:53:45', 'Ini Link Tugas', 90, NULL),
(2, '2209116054', 'poiuytrewq', '2024-01-11 16:54:17', 'Ini File Tugas', 90, NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `informasi`
--

CREATE TABLE `informasi` (
  `kd_informasi` char(5) NOT NULL,
  `tanggal` datetime NOT NULL,
  `judul_informasi` varchar(50) NOT NULL,
  `deskripsi_informasi` text NOT NULL,
  `tautan` text DEFAULT NULL,
  `usersid` char(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `informasi`
--

INSERT INTO `informasi` (`kd_informasi`, `tanggal`, `judul_informasi`, `deskripsi_informasi`, `tautan`, `usersid`) VALUES
('09zzF', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('0bIOm', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('12345', '2024-01-11 16:54:42', 'Modul Data Mining - CRISPDM', 'Digunakan untuk sarana belajar', 'ini tautannya', '2109116068'),
('1dM5b', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('2AIrI', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('2JZlk', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('2nKXg', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('342Z9', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('3DXd5', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('3hfwC', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('3Jzjz', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('4RgV0', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('510rF', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('54321', '2024-01-11 16:55:45', 'Pengingat Praktikum', 'Besok praktikum woy', NULL, '2109116095'),
('6HLpx', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('8bDOr', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('8Cpo2', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('9l3XS', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('9vGIo', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('AguTX', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('aI7wH', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('AXdvT', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('B77SG', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('bawNY', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('BdO0m', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('bo71M', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('bVTbM', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('c6EUc', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('CwAru', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('dINQY', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('EgW9r', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('EKpbD', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('exZpo', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('F6L8D', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('fGbni', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('Fzg8u', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('GWwa2', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('H07xh', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('HsGkd', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('ihpcV', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('j11vw', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('jlHwQ', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('jopJ1', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('JSAeD', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('juYcq', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('JWRuD', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('Kk8nt', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('l0rTE', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('lhW5T', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('LmuPo', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('mHmy5', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('mniLq', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('MrmxL', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('mUfd4', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('mv6Eh', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('NDeQf', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('nDw8N', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('nLp15', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('nW6q8', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('O7Hig', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('o8l78', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('oBAmV', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('ohZLc', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('OmH5m', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('oO451', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('paeF5', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('pav3W', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('PETiE', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('PmONS', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('QhYC5', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('QiBVG', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('qiKLG', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('qIq6t', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('qJGDe', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('QRIXt', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('RIBCK', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('rmpDa', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('tFnDd', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('tGasL', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('tiT71', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('u7FpA', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('u9viO', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('u9Z2t', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('Uf7Gu', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('uJnKW', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('V39DZ', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('WKw6K', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('X83M6', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('Xexx0', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('XtcU5', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('yIUUC', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('YpXXj', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('Yz0fJ', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('z9hGa', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('ze82Y', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068'),
('zNwpp', '2019-08-24 14:15:22', 'string', 'string', 'string', '2109116068');

-- --------------------------------------------------------

--
-- Struktur dari tabel `jadwal`
--

CREATE TABLE `jadwal` (
  `kd_jadwal` char(10) NOT NULL,
  `tanggal` date NOT NULL,
  `waktu_mulai` time NOT NULL,
  `waktu_selesai` time NOT NULL,
  `kelas` varchar(8) NOT NULL,
  `ruangan` varchar(30) NOT NULL,
  `materi` varchar(100) NOT NULL,
  `kd_matkul` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `jadwal`
--

INSERT INTO `jadwal` (`kd_jadwal`, `tanggal`, `waktu_mulai`, `waktu_selesai`, `kelas`, `ruangan`, `materi`, `kd_matkul`) VALUES
('79vv7QWoz1', '2024-01-13', '09:20:00', '10:50:00', 'A-1 2022', 'D308 - Lab Network', 'Pengenalan Data Mining', '1909036021'),
('cpQW3sHn1k', '2024-01-13', '09:20:00', '10:50:00', 'A-1 2022', 'D308 - Lab Network', 'Pengenalan Data Mining', '1909036021'),
('DxfM4koOkP', '2024-01-13', '09:20:00', '10:50:00', 'A-1 2022', 'D308 - Lab Network', 'Pengenalan Data Mining', '1909036021'),
('fvtgbyhnuj', '2024-01-13', '13:00:00', '14:30:00', 'A-2 2022', 'D308 - Lab Network', 'Pengenalan Data Mining', '1909036021'),
('n4yhcxoxY3', '2024-01-13', '09:20:00', '10:50:00', 'A-1 2022', 'D308 - Lab Network', 'Pengenalan Data Mining', '1909036021'),
('OX07UAyskx', '2024-01-13', '09:20:00', '10:50:00', 'A-1 2022', 'D308 - Lab Network', 'Pengenalan Data Mining', '1909036021'),
('qazwsxedcr', '2024-01-13', '09:20:00', '10:50:00', 'A-1 2022', 'D308 - Lab Network', 'Pengenalan Data Mining', '1909036021'),
('rcdexswzaq', '2024-01-13', '10:50:00', '12:20:00', 'A-2 2022', 'D309 - Lab Engineering', 'Pengenalan Web', '1909036023'),
('uXRX2OXUSE', '2024-01-13', '09:20:00', '10:50:00', 'A-1 2022', 'D308 - Lab Network', 'Pengenalan Data Mining', '1909036021');

-- --------------------------------------------------------

--
-- Struktur dari tabel `kehadiran`
--

CREATE TABLE `kehadiran` (
  `id` int(11) NOT NULL,
  `usersid` char(20) NOT NULL,
  `kd_jadwal` char(10) NOT NULL,
  `status` enum('Hadir','Tidak Hadir') NOT NULL,
  `keterangan` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `kehadiran`
--

INSERT INTO `kehadiran` (`id`, `usersid`, `kd_jadwal`, `status`, `keterangan`) VALUES
(1, '2209116004', 'rcdexswzaq', 'Hadir', '-'),
(2, '2209116054', 'qazwsxedcr', 'Hadir', '-');

-- --------------------------------------------------------

--
-- Struktur dari tabel `matkul_prak`
--

CREATE TABLE `matkul_prak` (
  `kd_matkul` char(10) NOT NULL,
  `nama_matkul` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `matkul_prak`
--

INSERT INTO `matkul_prak` (`kd_matkul`, `nama_matkul`) VALUES
('1909036020', 'Keamanan Informasi'),
('1909036021', 'Penggalian Data dan Analitika Bisnis'),
('1909036023', 'Perancangan & Pemrograman Web'),
('1909036050', 'Desain UI /UX'),
('1909036052', 'Desain UI /UX');

-- --------------------------------------------------------

--
-- Struktur dari tabel `nilai_akhir`
--

CREATE TABLE `nilai_akhir` (
  `id` int(11) NOT NULL,
  `usersid` char(20) NOT NULL,
  `kd_matkul` char(10) NOT NULL,
  `nilai_akhir` decimal(4,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `nilai_akhir`
--

INSERT INTO `nilai_akhir` (`id`, `usersid`, `kd_matkul`, `nilai_akhir`) VALUES
(1, '2209116004', '1909036023', 37.25),
(2, '2209116054', '1909036021', 54.00),
(3, '2209116006', '1909036050', 0.00),
(4, '2209116006', '1909036021', 0.00),
(5, '2209116006', '1909036023', 0.00),
(6, '2209116004', '1909036021', 54.00),
(8, '2209116004', '1909036050', 0.00),
(9, '2209116054', '1909036020', 0.00),
(10, '2209116004', '1909036020', 0.00),
(11, '2209116006', '1909036020', 0.00);

-- --------------------------------------------------------

--
-- Struktur dari tabel `tugas`
--

CREATE TABLE `tugas` (
  `kd_tugas` char(10) NOT NULL,
  `jenis_tugas` enum('Post Test','Proyek Akhir') NOT NULL,
  `nama_tugas` varchar(100) NOT NULL,
  `deskripsi_tugas` text NOT NULL,
  `tanggal_dibuat` datetime NOT NULL,
  `tanggal_pengumpulan` datetime NOT NULL,
  `kd_matkul` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `tugas`
--

INSERT INTO `tugas` (`kd_tugas`, `jenis_tugas`, `nama_tugas`, `deskripsi_tugas`, `tanggal_dibuat`, `tanggal_pengumpulan`, `kd_matkul`) VALUES
('asdfghjkll', 'Post Test', 'Post Test 2 - Web', 'Kerjakan', '2024-01-12 18:13:46', '2024-01-12 18:13:46', '1909036023'),
('poiuytrewq', 'Proyek Akhir', 'Proyek Akhir - Data Mining', 'Kerjakan PA ini!!!', '2024-01-11 16:50:43', '2024-01-18 23:50:43', '1909036021'),
('qwertyuiop', 'Post Test', 'Post Test 1 - Web', 'Buatlah web portofolio sederhana dengan HTML dan CSS saja!!!', '2024-01-11 16:50:43', '2024-01-18 23:50:43', '1909036023');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `userid` char(20) NOT NULL,
  `password` varchar(100) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `semester` varchar(20) NOT NULL,
  `praktikan` tinyint(1) NOT NULL,
  `asisten_laboratorium` tinyint(1) NOT NULL,
  `dosen` tinyint(1) NOT NULL,
  `kd_matkul` char(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`userid`, `password`, `nama`, `email`, `semester`, `praktikan`, `asisten_laboratorium`, `dosen`, `kd_matkul`) VALUES
('198608032019031006', 'password456', 'Putut Pamilih Widagdo, S.Kom., M. Kom', 'pututpamilih@gmail.com', 'Genap 2023/2024', 0, 0, 1, '1909036023'),
('198612182019031007', 'password909', 'Hario Jati Setyadi, S.Kom., M.Kom', 'hariojati.setyadi@ft.unmul.ac.id', 'Genap 2023/2024', 0, 0, 1, '1909036050'),
('199202122020121009', 'password098', 'Amin Padmo Azam Masa, S.Kom., M.Cs.', 'aminpadmo@ft.unmul.ac.id', 'Genap 2023/2024', 0, 0, 1, '1909036020'),
('199508272022031003', 'password567', 'Akhmad Irsyad S.T.,M.Kom', 'akhmadirsyad@ft.unmul.ac.id', 'Genap 2023/2024', 0, 0, 1, '1909036021'),
('2109116017', 'password000', 'Nur Inayah', 'nayanay@gmail.com', 'Genap 2023/2024', 1, 0, 0, NULL),
('2109116038', 'password000', 'Raihan Daiva Geralda', 'daivadai@gmail.com', 'daivadai@gmail.com', 1, 0, 0, NULL),
('2109116058', 'password987', 'Firzian Caesar Ananta', 'firzianfir@gmail.com', 'Genap 2023/2024', 0, 1, 0, '1909036020'),
('2109116068', 'password123', 'Wahyu Kesuma Bakti', 'kambingsegitiga@gmail.com', 'Genap 2023/2024', 0, 1, 0, '1909036021'),
('2109116077', 'password890', 'Muhammad Raza Daffa', 'daffadaf@gmail.com', 'Genap 2023/2024', 0, 1, 0, '1909036050'),
('2109116095', 'password678', 'Muhammad Novil Fahlevy', 'novilnovil@gmail.com', 'Genap 2023/2024', 0, 1, 0, '1909036023'),
('2209116004', 'password345', 'Novianti Safitri', 'novinov@gmail.com', 'Genap 2023/2024', 1, 1, 0, NULL),
('2209116006', 'password789', 'Dinnuhoni Trahutomo', 'dinnudin@gmail.com', 'Genap 2023/2024', 1, 0, 0, NULL),
('2209116054', 'password234', 'Dera Kayla', 'derader@gmail.com', 'Genap 2023/2024', 1, 0, 0, NULL);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `detail_pengumpulan`
--
ALTER TABLE `detail_pengumpulan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usersid` (`usersid`,`kd_tugas`),
  ADD KEY `detail_pengumpulan_tugas` (`kd_tugas`);

--
-- Indeks untuk tabel `informasi`
--
ALTER TABLE `informasi`
  ADD PRIMARY KEY (`kd_informasi`),
  ADD KEY `informasi_praktikum` (`usersid`);

--
-- Indeks untuk tabel `jadwal`
--
ALTER TABLE `jadwal`
  ADD PRIMARY KEY (`kd_jadwal`),
  ADD KEY `jadwal_matkul` (`kd_matkul`);

--
-- Indeks untuk tabel `kehadiran`
--
ALTER TABLE `kehadiran`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usersid` (`usersid`,`kd_jadwal`),
  ADD KEY `praktikan_kehadiran` (`kd_jadwal`);

--
-- Indeks untuk tabel `matkul_prak`
--
ALTER TABLE `matkul_prak`
  ADD PRIMARY KEY (`kd_matkul`);

--
-- Indeks untuk tabel `nilai_akhir`
--
ALTER TABLE `nilai_akhir`
  ADD PRIMARY KEY (`id`),
  ADD KEY `usersid` (`usersid`,`kd_matkul`),
  ADD KEY `nilai_akhir_matkul` (`kd_matkul`);

--
-- Indeks untuk tabel `tugas`
--
ALTER TABLE `tugas`
  ADD PRIMARY KEY (`kd_tugas`),
  ADD KEY `tugas_matkul` (`kd_matkul`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userid`),
  ADD KEY `aslab_mengajar` (`kd_matkul`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `detail_pengumpulan`
--
ALTER TABLE `detail_pengumpulan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=83;

--
-- AUTO_INCREMENT untuk tabel `kehadiran`
--
ALTER TABLE `kehadiran`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `nilai_akhir`
--
ALTER TABLE `nilai_akhir`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `detail_pengumpulan`
--
ALTER TABLE `detail_pengumpulan`
  ADD CONSTRAINT `detail_pengumpulan_ibfk_143` FOREIGN KEY (`usersid`) REFERENCES `users` (`userid`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `detail_pengumpulan_ibfk_144` FOREIGN KEY (`kd_tugas`) REFERENCES `tugas` (`kd_tugas`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `informasi`
--
ALTER TABLE `informasi`
  ADD CONSTRAINT `informasi_ibfk_1` FOREIGN KEY (`usersid`) REFERENCES `users` (`userid`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `jadwal`
--
ALTER TABLE `jadwal`
  ADD CONSTRAINT `jadwal_ibfk_1` FOREIGN KEY (`kd_matkul`) REFERENCES `matkul_prak` (`kd_matkul`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `kehadiran`
--
ALTER TABLE `kehadiran`
  ADD CONSTRAINT `kehadiran_ibfk_143` FOREIGN KEY (`usersid`) REFERENCES `users` (`userid`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `kehadiran_ibfk_144` FOREIGN KEY (`kd_jadwal`) REFERENCES `jadwal` (`kd_jadwal`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `nilai_akhir`
--
ALTER TABLE `nilai_akhir`
  ADD CONSTRAINT `nilai_akhir_ibfk_143` FOREIGN KEY (`usersid`) REFERENCES `users` (`userid`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `nilai_akhir_ibfk_144` FOREIGN KEY (`kd_matkul`) REFERENCES `matkul_prak` (`kd_matkul`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `tugas`
--
ALTER TABLE `tugas`
  ADD CONSTRAINT `tugas_ibfk_1` FOREIGN KEY (`kd_matkul`) REFERENCES `matkul_prak` (`kd_matkul`) ON DELETE NO ACTION ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`kd_matkul`) REFERENCES `matkul_prak` (`kd_matkul`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
