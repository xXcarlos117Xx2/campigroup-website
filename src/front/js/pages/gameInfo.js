import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

export const GameInfo = () => {
    const { gameId } = useParams();
    const [gameInfo, setGameInfo] = useState(null);
    const [gameImages, setGameImages] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchGameData = async () => {
            const backendUrl = process.env.REACT_APP_BACKEND_URL;
            try {
                const [gameInfoResponse, gameImagesResponse] = await Promise.all([
                    fetch(`${backendUrl}api/game-info/${gameId}`),
                    fetch(`${backendUrl}api/game-images/${gameId}`),
                ]);

                if (gameInfoResponse.ok && gameImagesResponse.ok) {
                    const gameInfoData = await gameInfoResponse.json();
                    const gameImagesData = await gameImagesResponse.json();
                    setGameInfo(gameInfoData);
                    setGameImages(gameImagesData.images || []);
                } else {
                    console.error("Error al cargar los datos del juego o las imágenes");
                }
            } catch (error) {
                console.error("Error fetching game data:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchGameData();
    }, [gameId]);

    if (loading) {
        return <p>Cargando...</p>;
    }

    if (!gameInfo) {
        return <p>Error al cargar la información del juego.</p>;
    }

    return (
        <div className="container mt-5">
            <div className="row">
                {/* Columna izquierda para la información */}
                <div className="col-sm-12 col-md-6">
                    <div className="card h-100">
                        <div className="card-body">
                            <h5 className="card-title">{gameInfo.title}</h5>
                            <ul className="list-unstyled">
                                <li className="mb-2">
                                    <strong>Descripción:</strong> {gameInfo.description}
                                </li>
                                <li className="mb-2">
                                    <strong>Géneros:</strong> {gameInfo.genres.join(", ")}
                                </li>
                                <li className="mb-2">
                                    <strong>Fecha de lanzamiento:</strong> {gameInfo.release_date}
                                </li>
                                <li className="mb-2">
                                    <strong>Desarrollador:</strong> {gameInfo.developer}
                                </li>
                                <li className="mb-2">
                                    <strong>Publicador:</strong> {gameInfo.publisher}
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                {/* Columna derecha para las imágenes */}
                <div className="col-md-6 mt-5 mt-md-0">
                    <div className="row g-3">
                        {gameImages.map((image, index) => (
                            <div className="col-md-6" key={index}>
                                <div
                                    className="card"
                                    style={{
                                        maxWidth: "100%", // Anchura dinámica
                                        overflow: "hidden", // Evita que el contenido se desborde
                                    }}
                                >
                                    <img
                                        src={image.url}
                                        className="card-img-top"
                                        alt={image.caption || `Imagen ${index + 1}`}
                                        style={{
                                            objectFit: "cover", // Escala la imagen correctamente
                                            width: "100%", // Asegura que ocupe todo el ancho
                                            height: "auto", // Asegura que ocupe todo el alto
                                        }}
                                    />
                                    <div className="card-body">
                                        <p className="card-text">
                                            {image.user ? `@${image.user}` : "@anónimo"}{" "}
                                            {image.caption ? `- ${image.caption}` : ""}
                                        </p>
                                        <p className="card-text text-muted">
                                            Subido el: {new Date(image.uploaded_at).toLocaleDateString()}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};
