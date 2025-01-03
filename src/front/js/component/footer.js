import React, { Component } from "react";

export const Footer = () => (
	<footer className="footer mt-auto max-vh-50 py-3 border-top bg-dark" data-bs-theme="dark">
	<div className="container">
	  <ul className="nav justify-content-center list-unstyled d-flex">
		<li className="ms-3"><a className="text-body-secondary" href="http://www.twitter.com/xXcarlos117Xx2"><i className="fa-lg fab fa-twitter-square"></i></a></li>
		<li className="ms-3"><a className="text-body-secondary" href="http://www.linkedin.com/in/xXcarlos117Xx2"><i className="fa-lg fab fa-linkedin"></i></a></li>
		<li className="ms-3"><a className="text-body-secondary" href="http://www.github.com/xXcarlos117Xx2"><i className="fa-lg fab fa-github-square"></i></a></li>
	  </ul>
	  <p className="text-center text-muted mt-2">
		<span>Campigroup© 2024<br/></span>
		<span>Todos los derechos reservados.</span>
	  </p>
	</div>
  </footer>
);
