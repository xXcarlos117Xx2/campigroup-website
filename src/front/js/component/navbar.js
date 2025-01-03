import React, { useContext } from "react";
import { Context } from "../store/appContext";
import { Link } from "react-router-dom";
import clan_logo from "../../img/clan_logo.png";

export const Navbar = () => {

    const { store, actions } = useContext(Context);

    return (
        <nav className="navbar navbar-expand-lg bg-dark" data-bs-theme="dark">
            <div className="container-fluid">
                {/* Link al Home */}
                <Link className="navbar-brand" to="/">
                    <img src={clan_logo} alt="Logo" style={{ maxWidth: "46px" }} />
                    <span className="mx-2">Campigroup</span>
                </Link>
                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarTogglerDemo02"
                    aria-controls="navbarTogglerDemo02"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarTogglerDemo02">
                    <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                        <li className="nav-item">
                            <Link className="nav-link active" to="/">Home</Link>
                        </li>
                    </ul>
                    {store.isLogin ? (
                        <button className="btn btn-danger" onClick={() => actions.logout()}>Logout</button>
                    ) : (
                        <>
                            <button className="disabled btn btn-success mx-2" onClick={() => actions.login()}>Login</button>
                            <button className="disabled btn btn-success mx-2" onClick={() => actions.register()}>Register</button>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};
