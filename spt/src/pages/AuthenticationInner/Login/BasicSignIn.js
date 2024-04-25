import React from 'react';
import { Link } from 'react-router-dom';
import { Card, CardBody, Col, Container, Input, Label, Row,Button } from 'reactstrap';
import ParticlesAuth from "../ParticlesAuth";


//import images
import logoLight from "../../../assets/images/logo-light.png";


const BasicSignIn = () => {
document.title="Login | SPT";
    return (
        <React.Fragment>
            <ParticlesAuth>
                <div className="auth-page-content">                
                    <Container>
                        <Row>
                            <Col lg={12}>
                                <div className="text-center mt-sm-5 mb-4 text-white-50">
                                    <div>
                                        <Link to="/" className="d-inline-block auth-logo">
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
                                            <h5 className="text-primary">Bienvenue !</h5>
                                            <p className="text-muted">Inscrivez-vous pour continuer à SPT.</p>
                                        </div>
                                        <div className="p-2 mt-4">
                                            <form action="#">

                                                <div className="mb-3">
                                                    <Label htmlFor="username" className="form-label">Username</Label>
                                                    <Input type="text" className="form-control" id="username" placeholder="Saisiez username" />
                                                </div>

                                                <div className="mb-3">
                                                    <div className="float-end">
                                                        <Link to="/auth-pass-reset-basic" className="text-muted">Vous avez oublié votre mot de passe?</Link>
                                                    </div>
                                                    <Label className="form-label" htmlFor="password-input">Mot de passe</Label>
                                                    <div className="position-relative auth-pass-inputgroup mb-3">
                                                        <Input type="password" className="form-control pe-5 password-input" placeholder="Saisiez votre Mot de passe" id="password-input" />
                                                        <button className="btn btn-link position-absolute end-0 top-0 text-decoration-none text-muted password-addon" type="button" id="password-addon"><i className="ri-eye-fill align-middle"></i></button>
                                                    </div>
                                                </div>

                                                <div className="form-check">
                                                    <Input className="form-check-input" type="checkbox" value="" id="auth-remember-check" />
                                                    <Label className="form-check-label" htmlFor="auth-remember-check">Souviens-toi de moi</Label>
                                                </div>

                                                <div className="mt-4">
                                                    <Button color="success" className="btn btn-success w-100" type="submit">Se connecter </Button>
                                                </div>

                                                
                                            </form>
                                        </div>
                                    </CardBody>
                                </Card>

                                <div className="mt-4 text-center">
                                    <p className="mb-0">Vous n'avez pas de compte? <Link to="/auth-signup-basic" className="fw-semibold text-primary text-decoration-underline"> Créer </Link> </p>
                                </div>

                            </Col>
                        </Row>
                    </Container>
                </div>
            </ParticlesAuth>
        </React.Fragment>
    );
};

export default BasicSignIn;