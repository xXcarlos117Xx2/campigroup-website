import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

export const Home = () => {
	const [servers, setServers] = useState([]);

	useEffect(() => {
		const fetchServersStatus = async () => {
			const backendUrl = process.env.REACT_APP_BACKEND_URL; // URL del backend desde el .env
			try {
				const response = await fetch(`${backendUrl}api/server-status`);
				if (response.ok) {
					const data = await response.json();
					setServers(data.servers); // Guardamos el array de servidores en el estado
				} else {
					console.error("Error al cargar los servidores");
				}
			} catch (error) {
				console.error("Error fetching servers:", error);
			}
		};

		fetchServersStatus();
	}, []);

	return (
		<div className="text-center mt-5">
			<h1>Estado de los Servidores</h1>
			<div className="container">
				<div className="row">
					{servers.map((server, index) => (
						<div className="col-md-4 my-2" key={index}>
							<div className="card">
								<div className="card-body">
									<h5 className="card-title">{server.name}</h5>
									<p className="card-text">Juego ID: {server.game_id}</p>
									<p className="card-text">IP: {server.ip_address}:{server.port}</p>
									<p className="card-text">Estado: {server.status}</p>
								</div>
								<div className="card-footer">
									<Link to={`/game-info/${server.game_id}`} className="btn btn-primary">
										Ver más información
									</Link>
								</div>
							</div>
						</div>
					))}
				</div>
			</div>
		</div>
	);
};
