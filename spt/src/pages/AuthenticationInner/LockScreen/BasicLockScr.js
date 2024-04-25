import React from 'react';
import { Link } from 'react-router-dom';
import { Button, Card, CardBody, Col, Container, Row } from 'reactstrap';
import ParticlesAuth from "../ParticlesAuth";

//import images
import logoLight from "../../../assets/images/logo-light.png";
import avatar1 from "../../../assets/images/users/avatar-1.jpg";


const BasicLockScreen = () => {
document.title="Lock Screen | SPT";
    return (
        <React.Fragment>
            <div className="auth-page-content">
                <div className="auth-page-wrapper">
                    <ParticlesAuth>
                        <div className="auth-page-content">
                            <Container>
                                <Row>
                                    <Col lg={12}>
                                        <div className="text-center mt-sm-5 mb-4 text-white-50">
                                            <div>
                                                <Link to="/dashboard" className="d-inline-block auth-logo">
                                                    <img src={logoLight} alt="" height="20" />
                                                </Link>
                                            </div>
                                        </div>
                                    </Col>
                                </Row>

                                <Row className="justify-content-center">
                                    <Col md={8} lg={6} xl={5}>
                                        <Card className="mt-4">
                                            <CardBody className="p-4">
                                                <div className="text-center mt-2">
                                                    <h5 className="text-primary">Écran de verrouillage</h5>
                                                    <p className="text-muted">Saisissez votre mot de passe pour débloquer l'écran!</p>
                                                </div>
                                                
                                                <div className="p-2 mt-4">
                                                    <form>
                                                        <div className="mb-3">
                                                            <label className="form-label" htmlFor="userpassword">Mot de passe</label>
                                                            <input type="password" className="form-control" id="userpassword" placeholder="Enter password" required />
                                                        </div>
                                                        <div className="mb-2 mt-4">
                                                            <Button color="success" className="w-100" type="submit">Déverrouiller</Button>
                                                        </div>
                                                    </form>
                                                </div>
                                            </CardBody>
                                        </Card>
                                        <div className="mt-4 text-center">
                                            <p className="mb-0">Not you ? return <Link to="/auth-signin-basic" className="fw-semibold text-primary text-decoration-underline"> Se connecter </Link> </p>
                                        </div>
                                    </Col>
                                </Row>
                            </Container>
                        </div>
                    </ParticlesAuth>
                </div>
            </div>
        </React.Fragment>
    );
};

export default BasicLockScreen;