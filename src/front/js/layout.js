import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";

import { Home } from "./pages/home";
import injectContext from "./store/appContext";

import { Navbar } from "./component/navbar";
import { Breadcrumbs } from "./component/breadcrumbs.js";
import { Footer } from "./component/footer";

//pages
import { GameInfo } from "./pages/gameInfo";


//create your first component
const Layout = () => {
    //the basename is used when your project is published in a subdirectory and not in the root of the domain
    // you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
    const basename = process.env.BASENAME || "";

    return (
        <div>
            <div className="app-container" style={{ display: "flex", flexDirection: "column", height: "100vh" }}>
            <BrowserRouter basename={basename}>
                    <Navbar />
                    <Breadcrumbs />
                    <div style={{ flexGrow: 1 }}>
                    <Routes>
                        <Route element={<Home />} path="/" />
                        <Route path="/game-info/:gameId" element={<GameInfo />} />
                    </Routes>
                    </div>
                    <Footer />
            </BrowserRouter>
            </div>
        </div>
    );
};

export default injectContext(Layout);
