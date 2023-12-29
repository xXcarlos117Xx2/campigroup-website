// React
import React from 'react';

// Bootstrap
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Offcanvas from 'react-bootstrap/Offcanvas';

// Data

export const Navegation = ({ data }) => {

    return (
        <>
            {['lg'].map((expand) => (
                <Navbar key={expand} expand={expand} className="bg-body-tertiary mb-3">
                    <Container fluid>
                        <Navbar.Brand href="#">Campigroup</Navbar.Brand>
                        <Navbar.Toggle aria-controls={`offcanvasNavbar-expand-${expand}`} />
                        <Navbar.Offcanvas
                            id={`offcanvasNavbar-expand-${expand}`}
                            aria-labelledby={`offcanvasNavbarLabel-expand-${expand}`}
                            placement="end"
                        >
                            <Offcanvas.Header closeButton>
                                <Offcanvas.Title id={`offcanvasNavbarLabel-expand-${expand}`}>
                                    Navegación
                                </Offcanvas.Title>
                            </Offcanvas.Header>
                            <Offcanvas.Body>
                                <Nav className="justify-content-end flex-grow-1 pe-3">
                                    <Nav.Link href="#">Indice</Nav.Link>
                                    <NavDropdown title="Juegos" id={`offcanvasNavbarDropdown-expand-${expand}`}>
                                        {Object.keys(data).map((category, index) => (
                                            <div key={index}>
                                                {data[category].map((game, gameIndex) => (
                                                    <NavDropdown.Item key={`${category}-${gameIndex}`} href={`${game.title}.html`}>
                                                        {game.title}
                                                    </NavDropdown.Item>
                                                ))}
                                                {index < Object.keys(data).length - 1 && <NavDropdown.Divider />}
                                            </div>
                                        ))}
                                    </NavDropdown>
                                </Nav>
                            </Offcanvas.Body>
                        </Navbar.Offcanvas>
                    </Container>
                </Navbar>
            ))}
        </>
    );
}