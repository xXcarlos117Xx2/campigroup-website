import React, { useContext } from "react";
import { Context } from "../store/appContext";

export const Home = () => {

	const tmpList = [
		{ name: "Minecraft", description: "Juego de construcción y aventuras", price: 26.95, URL: "https://www.minecraft.net/es-es" },
		{ name: "Among Us", description: "Juego de misterio y asesinatos", price: 3.99, URL: "https://store.steampowered.com/app/945360/Among_Us/" },
		{ name: "Terraria", description: "Juego de construcción y aventuras", price: 9.99, URL: "https://store.steampowered.com/app/105600/Terraria/" },
		{ name: "The Witcher 3", description: "Juego de aventuras y rol", price: 29.99, URL: "https://store.steampowered.com/app/292030/The_Witcher_3_Wild_Hunt/" },
		{ name: "Cyberpunk 2077", description: "Juego de aventuras y rol", price: 59.99, URL: "https://store.steampowered.com/app/1091500/Cyberpunk_2077/" }
	]
	return (
		<div className="text-center mt-5">
			<h1>Home</h1>
			<div className="container">
				<div className="row">
					{tmpList.map((item, index) => (
						<div className="col-md-4 my-2" key={index}>
							<div className="card">
								<img src="https://placehold.co/450" className="card-img-top" alt="..." />
								<div className="card-body">
									<h5 className="card-title">{item.name}</h5>
									<p className="card-text">{item.description}</p>
								</div>
								<div className="card-footer">
									<button className="btn btn-success">Ver información</button>
								</div>
							</div>
						</div>
					))}
				</div>
			</div>
		</div>
	);
};
