<?php
include "head.php";
?>
<!-- Body -->

<!-- Link Menu -->
<?php include "menu.php"; ?>

</div>
<br />

<div id="content">

	<!-- Page title -->
	<div class="page-title">
		<h5><i class="fa fa-desktop"></i> Halaman Admin</h5>
	</div>

	<div id="leftpanel">
		<div class="table_top">
			<div align="center"><span class="title_panel text-success"><b>Tugas Sistem Pendukung Keputusan</b></span> </div>
		</div>
		<div class="table_content">
			<div class="table_text">
				<div align="right"><span class="news_date" style="color: black;"><?php echo "[" . date("H:i:s") . "] - [" . date("d/M/Y") . "]"; ?></span></div> <br>
				<hr>
				<font color="black" align="center">
					<h6>"Seleksi Pemberian Bantuan Kepada Masyarakat Kurang Mampu"</h6>
				</font>
				<hr>
				<span class="news_date" style="text-align: center; color: black;">Latar Belakang</span> <br>
				<span class="news_text">
					<br>
					Dalam rangka meningkatkan efisiensi dan efektivitas pemberian bantuan kepada masyarakat yang membutuhkan, diperlukan sebuah platform yang dapat memudahkan proses seleksi penerima bantuan. Salah satu pendekatan yang dapat dilakukan adalah dengan melakukan survei langsung ke lokasi untuk memastikan keadaan rumah dan kebutuhan masyarakat yang bersangkutan. Namun, proses manual semacam ini seringkali memakan waktu dan sumber daya yang besar.

					Untuk mengatasi tantangan tersebut, dibangunlah sebuah platform digital berbasis website yang bertujuan untuk mengotomatisasi proses seleksi penerima bantuan. Melalui website ini, seorang petugas lapangan dapat ditugaskan untuk melakukan survei langsung ke lokasi. Setelah survei selesai, petugas akan memasukkan data hasil survei ke dalam sistem melalui website tersebut.

					Website ini memungkinkan pengguna untuk mengisi data penerima bantuan secara lengkap, termasuk informasi tentang kondisi rumah, kriteria kebutuhan, serta nilai-nilai kriteria yang relevan. Selain itu, website ini juga menyediakan fitur untuk melakukan analisis data secara otomatis, sehingga mempermudah proses pengambilan keputusan dalam menentukan penerima bantuan yang layak.

					Dengan adanya website ini, diharapkan proses seleksi penerima bantuan dapat dilakukan secara lebih efisien, transparan, dan akurat, sehingga bantuan yang diberikan dapat tepat sasaran dan memberikan dampak positif yang lebih besar bagi masyarakat yang membutuhkan.
				</span>
				<hr>
				<!-- <h5><i class='fa fa-user'></i>Nama : <?php echo "<font color='red'>[" . "$_SESSION[nama]" . "]</font>"; ?></h5> -->
				<!-- <br /><br /><br /><br /><br /><br /><br /><br /><br /> -->
			</div>
		</div>

		<br>

	</div>

	<br />
	<br />
	<!-- Footer -->
	<?php include "footer.php" ?>