// React
import React from 'react';

// Bootstrap
import { Container, Card, Button, Row, Col } from 'react-bootstrap';

export const GameCards = ({data}) => {
  return (
<Container>
      {Object.keys(data).map((category, index) => (
        <div className="border rounded bg-light my-4 p-1" key={index}>
          <h2 className="border-bottom p-2">{category}</h2>
          <Row className="justify-content-center align-items-stretch">
            {data[category].map((game, gameIndex) => (
              <Col key={`${index}-${gameIndex}`} className="my-4 d-flex justify-content-around">
                <Card style={{ width: '18rem' }}>
                  <Card.Img variant="top" src={game.image} style={{ maxWidth: '600px' }} />
                  <Card.Body>
                    <Card.Title>{game.title}</Card.Title>
                    <Card.Text>{game.description}</Card.Text>
                  </Card.Body>
                  <Card.Footer className="text-center">
                    <Button variant="primary" href={`${game.title}.html`}>
                      {game.label}
                    </Button>
                  </Card.Footer>
                </Card>
              </Col>
            ))}
          </Row>
        </div>
      ))}
    </Container>
  );
}