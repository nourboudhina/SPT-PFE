import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Card, CardBody, Col, Container, Row, Form, FormFeedback, Input, Button } from 'reactstrap';
import ParticlesAuth from "../ParticlesAuth";

//import images 
import logoLight from "../../../assets/images/logo-light.png";

//formik
import { useFormik } from 'formik';
import * as Yup from 'yup';

const BasicSignUp = () => {
    document.title = " SignUp | SPT";

    const [passwordShow, setPasswordShow] = useState(false);

    const validation = useFormik({
        enableReinitialize: true,

        initialValues: {
            password: "",
        },
        validationSchema: Yup.object({
            password: Yup.string()
            .min(8, 'Le mot de passe doit être au moins 8 caractères')
            .matches(RegExp('(.*[a-z].*)'), 'Au moins une lettre Miniscule')
            .matches(RegExp('(.*[A-Z].*)'), 'Au moins une lettre Majuscule')
            .matches(RegExp('(.*[0-9].*)'), 'Au moins un numéro')
            .required("Ce champ est requis"),
        }),
        onSubmit: (values) => {
            // console.log(values);
        }
    });

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
                                            <h5 className="text-primary">Créer un nouveau compte</h5>
                                            <p className="text-muted">Obtenez votre compte SPT maintenant</p>
                                        </div>
                                        <div className="p-2 mt-4">
                                            <Form onSubmit={validation.handleSubmit} className="needs-validation" action="#">

                                                <div className="mb-3">
                                                    <label htmlFor="useremail" className="form-label">Email <span className="text-danger">*</span></label>
                                                    <input type="email" className="form-control" id="useremail" placeholder="Saisiez votre email" required />
                                                    <div className="invalid-feedback">
                                                    Veuillez saisir votre email
                                                    </div>
                                                </div>
                                                <div className="mb-3">
                                                    <label htmlFor="username" className="form-label">Username <span className="text-danger">*</span></label>
                                                    <input type="text" className="form-control" id="username" placeholder="Saisiez username" required />
                                                    <div className="invalid-feedback">
                                                    Veuillez saisir votre username
                                                    </div>
                                                </div>

                                                <div className="mb-3">
                                                    <label className="form-label" htmlFor="password-input">Mot de passe</label>
                                                    <div className="position-relative auth-pass-inputgroup">
                                                        <Input
                                                            type={passwordShow ? "text" : "password"}
                                                            className="form-control pe-5 password-input"
                                                            placeholder="Saisiez votre Mot de passe"
                                                            id="password-input"
                                                            name="password"
                                                            value={validation.values.password}
                                                            onBlur={validation.handleBlur}
                                                            onChange={validation.handleChange}
                                                            invalid={validation.errors.password && validation.touched.password ? true : false}
                                                        />
                                                        {validation.errors.password && validation.touched.password ? (
                                                            <FormFeedback type="invalid">{validation.errors.password}</FormFeedback>
                                                        ) : null}
                                                        <Button color="link" onClick={() => setPasswordShow(!passwordShow)} className="position-absolute end-0 top-0 text-decoration-none text-muted password-addon" type="button"
                                                            id="password-addon"><i className="ri-eye-fill align-middle"></i></Button>
                                                    </div>
                                                </div>

                                                <div className="mb-4">
                                                    <p className="mb-0 fs-12 text-muted fst-italic">En vous inscrivant, vous acceptez le SPT
                                                        <Link to="#" className="text-primary text-decoration-underline fst-normal fw-medium">Conditions d'utilisation</Link></p>
                                                </div>

                                                <div id="password-contain" className="p-3 bg-light mb-2 rounded">
                                                <h5 className="fs-13">Le mot de passe doit contenir:</h5>
                                                <p id="pass-length" className="invalid fs-12 mb-2"><b>8 caractères minimum</b></p>
                                                <p id="pass-lower" className="invalid fs-12 mb-2">Au <b> moins </b> un lettre de (a-z)</p>
                                                <p id="pass-upper" className="invalid fs-12 mb-2">Au <b> moins </b> un lettre de (A-Z)</p>
                                                <p id="pass-number" className="invalid fs-12 mb-0">Au <b> moins </b> un nombre de (0-9)</p>
                                            </div>

                                                <div className="mt-4">
                                                    <button className="btn btn-success w-100" type="submit">Créer</button>
                                                </div>

                                                
                                            </Form>
                                        </div>
                                    </CardBody>
                                </Card>

                                <div className="mt-4 text-center">
                                    <p className="mb-0">Vous avez déjà un compte? <Link to="/auth-signin-basic" className="fw-semibold text-primary text-decoration-underline"> Se connecter </Link> </p>
                                </div>

                            </Col>
                        </Row>
                    </Container>
                </div>
            </ParticlesAuth>
        </React.Fragment>
    );
};

export default BasicSignUp;