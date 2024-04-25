import React from 'react';
import { Link } from 'react-router-dom';
import { Alert, Card, CardBody, Col, Container, Row, Form, Label, Input, FormFeedback } from 'reactstrap';
import ParticlesAuth from '../ParticlesAuth';
import logoLight from "../../../assets/images/logo-light.png";

//formik
import { useFormik } from 'formik';
import * as Yup from 'yup';

const BasicPasswReset = () => {
    document.title="Reset Password | SPT";

    const validation = useFormik({
        enableReinitialize: true,
        
        initialValues: {
            email: "",
        },
        validationSchema: Yup.object({
            email: Yup.string().required("Veuillez saisir votre Email")
            .matches("Veuillez inclure un @ dans l'adresse email"),
        }),
        onSubmit: (values) => {
            // console.log(values);
        }
    });

    return (
        <ParticlesAuth>
            <div className="auth-page-content">                
                <Container>
                    <Row>
                        <Col lg={12}>
                            <div className="text-center mt-sm-5 mb-4 text-white-50">
                                <div>
                                    <Link to="/#" className="d-inline-block auth-logo">
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
                                        <h5 className="text-primary">Vous avez oublié votre mot de passe?</h5>
                                        <p className="text-muted">Réinitialiser le mot de passe avec SPT</p>

                                        <lord-icon
                                            src="https://cdn.lordicon.com/rhvddzym.json"
                                            trigger="loop"
                                            colors="primary:#0ab39c"
                                            className="avatar-xl"
                                            style={{ width: "120px", height: "120px" }}>
                                        </lord-icon>
                                    </div>

                                    <Alert className="alert-borderless alert-warning text-center mb-2 mx-2" role="alert">
                                    Saisissez votre courriel et les instructions vous seront envoyées!
                                    </Alert>
                                    <div className="p-2">
                                        <Form onSubmit={validation.handleSubmit}>
                                            <div className="mb-4">
                                                <Label className="form-label">Email</Label>
                                                <Input 
                                                type="email" 
                                                className="form-control" 
                                                id="email"
                                                placeholder="Saisiez votre Email" 
                                                name="email"
                                                value={validation.values.email}
                                                onBlur={validation.handleBlur}
                                                onChange={validation.handleChange}
                                                invalid={validation.errors.email && validation.touched.email ? true : false}
                                                />
                                                {validation.errors.email && validation.touched.email ? (
                                                    <FormFeedback type="invalid">{validation.errors.email}</FormFeedback>
                                                ): null}
                                            </div>

                                            <div className="text-center mt-4">
                                                <button className="btn btn-success w-100" type="submit">Envoyer le lien </button>
                                            </div>
                                        </Form>
                                    </div>
                                </CardBody>
                            </Card>

                            <div className="mt-4 text-center">
                                <p className="mb-0">Attendez, je me souviens de mon mot de passe...  <Link to="/auth-signin-basic" className="fw-bold text-primary text-decoration-underline"> Cliquez ici </Link> </p>
                            </div>

                        </Col>
                    </Row>
                </Container>
            </div>
        </ParticlesAuth>
    );
};

export default BasicPasswReset;