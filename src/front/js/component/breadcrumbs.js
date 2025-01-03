import React from "react";
import { Link, useLocation } from "react-router-dom";

export const Breadcrumbs = () => {
    const location = useLocation();
    const pathnames = location.pathname.split("/").filter((x) => x);

    return (
        <nav className="ms-2 my-2" aria-label="breadcrumb">
            <ol className="breadcrumb">
                {/* Siempre incluir Home */}
                <li className="breadcrumb-item">
                    {pathnames.length > 0 ? (
                        <Link className="saber-blue" to="/">Home</Link>
                    ) : (
                        <span className="active">Home</span>
                    )}
                </li>

                {/* Mostrar breadcrumbs dinámicos */}
                {pathnames.map((value, index) => {
                    const isLast = index === pathnames.length - 1;
                    const isParameter = !isNaN(value) || value.includes("-");

                    // Ruta acumulativa hasta el punto actual
                    const to = `/${pathnames.slice(0, index + 1).join("/")}`;

                    return isLast ? (
                        <li key={to} className="breadcrumb-item active" aria-current="page">
                            {isParameter ? "Detalle" : value.charAt(0).toUpperCase() + value.slice(1)}
                        </li>
                    ) : (
                        <li key={to} className="breadcrumb-item">
                            {!isParameter ? (
                                <Link className="saber-blue" to={to}>
                                    {value.charAt(0).toUpperCase() + value.slice(1)}
                                </Link>
                            ) : (
                                <span>Detalle</span>
                            )}
                        </li>
                    );
                })}
            </ol>
        </nav>
    );
};
