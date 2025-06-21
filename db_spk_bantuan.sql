-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 22 Apr 2024 pada 15.18
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
-- Database: `db_spk_bantuan`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `admin`
--

CREATE TABLE `admin` (
  `id_user` int(5) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `nama` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `admin`
--

INSERT INTO `admin` (`id_user`, `username`, `password`, `nama`) VALUES
(1, 'admin', '21232f297a57a5a743894a0e4a801fc3', 'admin');

-- --------------------------------------------------------

--
-- Struktur dari tabel `himpunan`
--

CREATE TABLE `himpunan` (
  `id_himpunan` int(5) NOT NULL,
  `id_kriteria` int(5) NOT NULL,
  `namahimpunan` varchar(100) NOT NULL,
  `nilai` varchar(100) NOT NULL,
  `keterangan` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `himpunan`
--

INSERT INTO `himpunan` (`id_himpunan`, `id_kriteria`, `namahimpunan`, `nilai`, `keterangan`) VALUES
(25, 1, 'Tidak Lulus SD', '25', 'Sangat Baik'),
(26, 1, 'SD-SMA', '50', 'Baik'),
(27, 1, 'S1', '75', 'Cukup'),
(28, 1, 'S2-S3', '100', 'Kurang'),
(29, 2, 'Rp. 0 / Tidak ada pekerjaan', '25', 'Sangat Baik'),
(30, 2, 'Rp. 1.500.000 - Rp. 2.500.000', '50', 'Baik'),
(31, 2, 'Rp. 2.600.000 - Rp. 5.000.000', '75', 'Cukup'),
(32, 2, 'Penghasilan > Rp. 5.000.000', '100', 'Kurang'),
(33, 3, 'Lantai: Tanah, Tembok: Kayu, Atap: Bocor', '25', 'Sangat Baik'),
(34, 3, 'Lantai: Tanah, Tembok: Beton, Atap: Bocor', '50', 'Baik'),
(35, 3, 'Lantai: Beton, Tembok: Beton, Atap: Tidak Bocor', '75', 'Cukup'),
(36, 3, 'Lantai: Keramik, Tembok: Keramik, Atap: Tidak Bocor', '100', 'Kurang'),
(37, 4, '1 anak', '25', 'Kurang'),
(38, 4, '2-3 Anak', '50', 'Cukup'),
(39, 4, '4 Anak', '75', 'Baik'),
(40, 4, 'Jml. Tanggungan > 5 Anak', '100', 'Sangat Baik'),
(41, 5, 'Usia < 21 Tahun', '25', 'Kurang'),
(42, 5, '21 - 30 Tahun', '50', 'Cukup'),
(43, 5, '31 - 40 Tahun', '75', 'Baik'),
(44, 5, 'Usia > 40 Tahun', '100', 'Sangat Baik');

-- --------------------------------------------------------

--
-- Struktur dari tabel `klasifikasi`
--

CREATE TABLE `klasifikasi` (
  `id_klasifikasi` int(5) NOT NULL,
  `id_penerima` varchar(10) DEFAULT NULL,
  `jml_tanggungan` double NOT NULL,
  `pend_terakhir` double DEFAULT NULL,
  `penghasilan_ortu` double NOT NULL,
  `kond_rumah` double DEFAULT NULL,
  `usia` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `klasifikasi`
--

INSERT INTO `klasifikasi` (`id_klasifikasi`, `id_penerima`, `jml_tanggungan`, `pend_terakhir`, `penghasilan_ortu`, `kond_rumah`, `usia`) VALUES
(37, '', 50, 25, 50, 50, 75),
(38, 'CPB~001', 100, 50, 50, 50, 75),
(39, 'CPB~002', 25, 75, 100, 100, 25),
(40, 'CPB~003', 25, 25, 25, 25, 100),
(41, 'CPB~004', 75, 100, 100, 100, 75),
(42, 'CPB~005', 100, 100, 75, 75, 25),
(43, 'CPB~006', 50, 25, 50, 25, 100),
(44, 'CPB~007', 50, 50, 50, 50, 50),
(45, 'CPB~008', 25, 25, 25, 25, 75),
(46, 'CPB~009', 75, 25, 75, 75, 50),
(47, 'CPB~010', 25, 100, 100, 100, 25),
(48, 'CPB~011', 50, 50, 50, 50, 75),
(49, 'CPB~012', 25, 75, 75, 50, 25),
(50, 'CPB~013', 50, 50, 25, 25, 50),
(51, 'CPB~014', 25, 100, 25, 100, 75),
(52, 'CPB~015', 75, 75, 75, 100, 50),
(53, 'CPB~016', 25, 50, 50, 50, 25),
(54, 'CPB~017', 25, 50, 100, 100, 25),
(55, 'CPB~018', 50, 75, 25, 25, 50),
(56, 'CPB~019', 100, 100, 75, 75, 25),
(57, 'CPB~020', 25, 100, 50, 100, 100);

-- --------------------------------------------------------

--
-- Struktur dari tabel `kriteria`
--

CREATE TABLE `kriteria` (
  `id_kriteria` int(5) NOT NULL,
  `namakriteria` varchar(100) NOT NULL,
  `atribut` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `kriteria`
--

INSERT INTO `kriteria` (`id_kriteria`, `namakriteria`, `atribut`) VALUES
(1, 'Pendidikan Terakhir', 'Cost'),
(2, 'Penghasilan', 'Cost'),
(3, 'Kondisi Rumah', 'Cost'),
(4, 'Jumlah Tanggungan', 'Benefit'),
(5, 'Usia', 'Benefit');

-- --------------------------------------------------------

--
-- Struktur dari tabel `penerima`
--

CREATE TABLE `penerima` (
  `id_penerima` varchar(10) NOT NULL,
  `nama_penerima` varchar(100) DEFAULT NULL,
  `asal` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data untuk tabel `penerima`
--

INSERT INTO `penerima` (`id_penerima`, `nama_penerima`, `asal`) VALUES
('CPB~001', 'Sutedi', 'Teluk Betung Timur'),
('CPB~002', 'Bejo', 'Bandar Lampung'),
('CPB~003', 'Rizki', 'Rajabasa'),
('CPB~004', 'Ipul', 'Sekarame'),
('CPB~005', 'Rama', 'Natar'),
('CPB~006', 'Ijat', 'Teluk Betung Timur'),
('CPB~007', 'Bung', 'Way Kandis'),
('CPB~008', 'Ipin', 'Way Halim'),
('CPB~009', 'Upin', 'Natar'),
('CPB~010', 'Ehsan', 'Teluk Betung Timur'),
('CPB~011', 'Jarjit', 'Sekarame'),
('CPB~012', 'Bunga', 'Bandar Lampung'),
('CPB~013', 'Siti', 'Sekarame'),
('CPB~014', 'Diaz', 'Way Kandis'),
('CPB~015', 'Pili', 'Rajabasa'),
('CPB~016', 'Ghifari', 'Way Halim'),
('CPB~017', 'Mail', 'Teluk Betung Timur'),
('CPB~018', 'Alya', 'Way Halim'),
('CPB~019', 'Mujlis', 'Mesuji'),
('CPB~020', 'Enday', 'Teluk Betung Timur'),
('CPB~021', 'edni', 'Teluk Betung Timur');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id_user`);

--
-- Indeks untuk tabel `himpunan`
--
ALTER TABLE `himpunan`
  ADD PRIMARY KEY (`id_himpunan`);

--
-- Indeks untuk tabel `klasifikasi`
--
ALTER TABLE `klasifikasi`
  ADD PRIMARY KEY (`id_klasifikasi`);

--
-- Indeks untuk tabel `kriteria`
--
ALTER TABLE `kriteria`
  ADD PRIMARY KEY (`id_kriteria`);

--
-- Indeks untuk tabel `penerima`
--
ALTER TABLE `penerima`
  ADD PRIMARY KEY (`id_penerima`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `admin`
--
ALTER TABLE `admin`
  MODIFY `id_user` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `himpunan`
--
ALTER TABLE `himpunan`
  MODIFY `id_himpunan` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT untuk tabel `klasifikasi`
--
ALTER TABLE `klasifikasi`
  MODIFY `id_klasifikasi` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT untuk tabel `kriteria`
--
ALTER TABLE `kriteria`
  MODIFY `id_kriteria` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
