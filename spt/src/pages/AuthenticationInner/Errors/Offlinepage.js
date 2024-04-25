import React from 'react';
import { Button, Card, CardBody, Col, Container, Row } from 'reactstrap';

// Import Images
import offlineImg from "../../../assets/images/auth-offline.gif";

const Offlinepage = () => {
    document.title = "Offline Page | SPT";
    return (
        <React.Fragment>
            <div className="auth-page-wrapper auth-bg-cover py-5 d-flex justify-content-center align-items-center min-vh-100">
                <div className="bg-overlay"></div>
                <div className="auth-page-content overflow-hidden pt-lg-5">
                    <Container>
                        <Row className="justify-content-center">
                            <Col xl={5}>
                                <Card className="overflow-hidden">
                                    <CardBody className="p-4">
                                        <div className="text-center">
                                            <img src={offlineImg} alt="" height="210" />
                                            <h3 className="mt-4 fw-semibold">Nous sommes actuellement hors ligne</h3>
                                            <p className="text-muted mb-4 fs-14">Nous ne pouvons pas vous montrer ces images parce que vous n'êtes pas connecté à Internet. Lorsque vous êtes de retour en ligne, rafraîchissez la page ou appuyez sur le bouton ci-dessous</p>
                                            <Button color="success" className="btn-border"
                                                // onClick={() => "window.location.href=window.location.href"}
                                            ><i className="ri-refresh-line align-bottom"></i> Refresh</Button>
                                        </div>
                                    </CardBody>
                                </Card>
                            </Col>
                        </Row>
                    </Container>
                </div>
            </div>
        </React.Fragment>
    );
};

export default Offlinepage;