import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button, Card, CardBody, Col, Container, Row, Form, Input, Label, FormFeedback } from 'reactstrap';
import ParticlesAuth from '../ParticlesAuth';
import logoLight from "../../../assets/images/logo-light.png";

//formik
import { useFormik } from 'formik';
import * as Yup from 'yup';

const BasicPasswCreate = () => {

    document.title = "Create New Password | SPT";

    const [passwordShow, setPasswordShow] = useState(false);
    const [confrimPasswordShow, setConfrimPasswordShow] = useState(false);

    const validation = useFormik({
        enableReinitialize: true,

        initialValues: {
            password: "",
            confrim_password: "",
        },
        validationSchema: Yup.object({
            password: Yup.string()
                .min(8, 'Le mot de passe doit être au moins 8 caractères')
                .matches(RegExp('(.*[a-z].*)'), 'Au moins une lettre Miniscule')
                .matches(RegExp('(.*[A-Z].*)'), 'Au moins une lettre Majuscule')
                .matches(RegExp('(.*[0-9].*)'), 'Au moins un numéro')
                .required("Ce champ est requis"),
            confrim_password: Yup.string()
                .when("Mot de passe", {
                    is: (val) => (val && val.length > 0 ? true : false),
                    then: Yup.string().oneOf(
                        [Yup.ref("Mot de passe")],
                        "Les deux mots de passe doivent être les mêmes"
                    ),
                })
                .required("Confirmer le mot de passe requis"),
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
                                        <h5 className="text-primary">Créer un nouveau mot de passe</h5>
                                        <p className="text-muted">Votre nouveau mot de passe doit être différent de celui utilisé précédemment.</p>
                                    </div>

                                    <div className="p-2">
                                        <Form onSubmit={validation.handleSubmit} action="/auth-signin-basic">
                                            <div className="mb-3">
                                                <Label className="form-label" htmlFor="password-input">Mot de passe</Label>
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
                                                <div id="passwordInput" className="form-text">Le mot de passe doit être au moins 8 caractères</div>
                                            </div>

                                            <div className="mb-3">
                                                <Label className="form-label" htmlFor="confirm-password-input">Confirmer le mot de passe</Label>
                                                <div className="position-relative auth-pass-inputgroup mb-3">
                                                    <Input
                                                        type={confrimPasswordShow ? "text" : "password"}
                                                        className="form-control pe-5 password-input"
                                                        placeholder="Confirm password"
                                                        id="confirm-password-input"
                                                        name="confrim_password"
                                                        value={validation.values.confrim_password}
                                                        onBlur={validation.handleBlur}
                                                        onChange={validation.handleChange}
                                                        invalid={validation.errors.confrim_password && validation.touched.confrim_password ? true : false}
                                                    />
                                                    {validation.errors.confrim_password && validation.touched.confrim_password ? (
                                                        <FormFeedback type="invalid">{validation.errors.confrim_password}</FormFeedback>
                                                    ) : null}
                                                    <Button color="link" onClick={() => setConfrimPasswordShow(!confrimPasswordShow)} className="position-absolute end-0 top-0 text-decoration-none text-muted password-addon" type="button">
                                                        <i className="ri-eye-fill align-middle"></i></Button>
                                                </div>
                                            </div>

                                            <div id="password-contain" className="p-3 bg-light mb-2 rounded">
                                                <h5 className="fs-13">Le mot de passe doit contenir:</h5>
                                                <p id="pass-length" className="invalid fs-12 mb-2"><b>8 caractères minimum</b></p>
                                                <p id="pass-lower" className="invalid fs-12 mb-2">Au <b> moins </b> un lettre de (a-z)</p>
                                                <p id="pass-upper" className="invalid fs-12 mb-2">Au <b> moins </b> un lettre de (A-Z)</p>
                                                <p id="pass-number" className="invalid fs-12 mb-0">Au <b> moins </b> un nombre de (0-9)</p>
                                            </div>

                                            <div className="form-check">
                                                <Input className="form-check-input" type="checkbox" value="" id="auth-remember-check" />
                                                <Label className="form-check-label" htmlFor="auth-remember-check">Souviens-toi de moi</Label>
                                            </div>

                                            <div className="mt-4">
                                                <Button color="success" className="w-100" type="submit">Réinitialiser </Button>
                                            </div>
                                        </Form>
                                    </div>
                                </CardBody>
                            </Card>
                            <div className="mt-4 text-center">
                                <p className="mb-0">Attendez, je me souviens de mon mot de passe...  <Link to="/auth-signin-basic" className="fw-semibold text-primary text-decoration-underline"> Cliquez ici  </Link> </p>
                            </div>
                        </Col>
                    </Row>
                </Container>
            </div>
        </ParticlesAuth>
    );
};

export default BasicPasswCreate;