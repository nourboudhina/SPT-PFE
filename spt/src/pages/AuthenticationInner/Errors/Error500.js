import React from 'react';
import { Link } from 'react-router-dom';
import { Col, Container, Row } from 'reactstrap';

// Import Images
import error500 from "../../../assets/images/error500.png";

const Error500 = () => {
document.title ="500 Error | SPT";
    return (
        <React.Fragment>
            
            
            <div className="auth-page-wrapper py-5 d-flex justify-content-center align-items-center min-vh-100">
                <div className="auth-page-content overflow-hidden p-0">
                    <Container fluid={true}>
                        <Row className="justify-content-center">
                            <Col xl={4} className="text-center">
                                <div className="error-500 position-relative">
                                    <img src={error500} alt="" className="img-fluid error-500-img error-img" />
                                    <h1 className="title text-muted">500</h1>
                                </div>
                                <div>
                                    <h4>Erreur de serveur interne!</h4>
                                    <p className="text-muted w-75 mx-auto">Erreur 500 du serveur. Nous ne savons pas exactement ce qui s'est passé, mais nos serveurs disent que quelque chose ne va pas.</p>
                                    <Link to="/dashboard" className="btn btn-success"><i className="mdi mdi-home me-1"></i>Retour</Link>
                                </div>
                            </Col>
                        </Row>
                    </Container>
                </div>
            </div>
        </React.Fragment>
    );
};

export default Error500;