import React, { Component } from "react";

export const Footer = () => (
	<footer className="bg-dark text-white text-center py-4">
		<div className="container">
			<div className="row">
				<div className="col-md-4 mb-3 mb-md-0">
					<h5>About Us</h5>
					<p>
						lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl nec consequat
					</p>
				</div>
				<div className="col-md-4 mb-3 mb-md-0">
					<h5>Contact</h5>
					<ul className="list-unstyled">
						<li><a href="mailto:carlos117@campigroup.es" className="text-white">carlos117@campigroup.es</a></li>
					</ul>
				</div>
				<div className="col-md-4">
					<h5>Follow Us</h5>
					<a href="#" className="text-white me-4"><i className="fab fa-facebook-f"></i></a>
					<a href="#" className="text-white me-4"><i className="fab fa-twitter"></i></a>
					<a href="#" className="text-white"><i className="fab fa-instagram"></i></a>
				</div>
			</div>
			<div className="row mt-4">
				<div className="col-12">
					<p className="mb-0">&copy; 2024 Campigroup.es. All rights reserved.</p>
				</div>
			</div>
		</div>
	</footer>
);
