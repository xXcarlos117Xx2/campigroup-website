import React, { useContext } from "react";
import { Context } from "../store/appContext";
import { Link } from "react-router-dom";
import clan_logo from "../../img/clan_logo.png";

export const Navbar = () => {

	const { store, actions } = useContext(Context);

	return (
		<nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark">
			<div class="container-fluid">
				<a class="navbar-brand" href="#"><img src={clan_logo} style={{maxWidth: "46px" }}/><span className="mx-2">Campigroup</span></a>
				<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02" aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
					<span class="navbar-toggler-icon"></span>
				</button>
				<div class="collapse navbar-collapse" id="navbarTogglerDemo02">
					<ul class="navbar-nav me-auto mb-2 mb-lg-0">
						<li class="nav-item">
							<a class="nav-link active" aria-current="#" href="#"></a>
						</li>
					</ul>
					{store.isLogin ?
						<button className="btn btn-danger" onClick={() => actions.logout()}>Logout</button> :
						<>
							<button className="btn btn-success mx-2" onClick={() => actions.login()}>Login</button>
							<button className="btn btn-success mx-2" onClick={() => actions.register()}>Register</button>
						</>
					}
				</div>
			</div>
		</nav>
	);
};
