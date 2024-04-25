import React, { useEffect } from "react";
import { Row, Col, CardBody, Card, Alert, Container, Input, Label, Form, FormFeedback } from "reactstrap";
import * as Yup from "yup";
import { useFormik } from "formik";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { registerUser, apiError, resetRegisterFlag } from "../../store/actions";
import { useSelector, useDispatch } from "react-redux";
import { Link, useHistory } from "react-router-dom";
import logoLight from "../../assets/images/logo-light.png";
import ParticlesAuth from "../AuthenticationInner/ParticlesAuth";

const Register = () => {
    const history = useHistory();
    const dispatch = useDispatch();

    const validation = useFormik({
        enableReinitialize: true,
        initialValues: {
            email: '',
            first_name: '',
            phone: '',
            password: '',
            confirm_password: ''
        },
        validationSchema: Yup.object({
            email: Yup.string().required("Saisissez votre email"),
            first_name: Yup.string().required("Saisissez votre nom d'utilisateur"),
            phone: Yup.string().required("Saisissez votre numéro de téléphone"),
            password: Yup.string().required("Saisissez votre mot de passe"),
            confirm_password: Yup.string().when("password", {
                is: val => (val && val.length > 0 ? true : false),
                then: Yup.string().oneOf(
                    [Yup.ref("password")],
                    "La confirmation du mot de passe ne correspond pas"
                )
            })
        }),
        onSubmit: (values) => {
            dispatch(registerUser(values));
        }
    });

    const { error, registrationError, success } = useSelector(state => ({
        registrationError: state.Account.registrationError,
        success: state.Account.success,
        error: state.Account.error
    }));

    useEffect(() => {
        dispatch(apiError(""));
    }, [dispatch]);

    useEffect(() => {
        if (success) {
            setTimeout(() => history.push("login"), 3000);
        }

        setTimeout(() => {
            dispatch(resetRegisterFlag());
        }, 3000);

    }, [dispatch, success, error, history]);

    document.title = "Inscription | SPT";

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
                                            <Form
                                                onSubmit={(e) => {
                                                    e.preventDefault();
                                                    validation.handleSubmit();
                                                    return false;
                                                }}
                                                className="needs-validation"
                                                action="#"
                                            >

                                                {success && (
                                                    <Alert color="success">
                                                        Utilisateur enregistré avec succès et redirigez-vous vers la page de connexion...
                                                    </Alert>
                                                )}

                                                {error && (
                                                    <Alert color="danger">
                                                        E-mail a été enregistré avant. Veuillez utiliser une autre adresse e-mail.
                                                    </Alert>
                                                )}

                                                <div className="mb-3">
                                                    <Label htmlFor="email" className="form-label">Email <span className="text-danger">*</span></Label>
                                                    <Input
                                                        id="email"
                                                        name="email"
                                                        className="form-control"
                                                        placeholder="Saisie adresse email"
                                                        type="email"
                                                        onChange={validation.handleChange}
                                                        onBlur={validation.handleBlur}
                                                        value={validation.values.email || ""}
                                                        invalid={validation.touched.email && !!validation.errors.email}
                                                    />
                                                    <FormFeedback type="invalid">{validation.errors.email}</FormFeedback>
                                                </div>

                                                <div className="mb-3">
                                                    <Label htmlFor="first_name" className="form-label">Nom d'utilisateur <span className="text-danger">*</span></Label>
                                                    <Input
                                                        id="first_name"
                                                        name="first_name"
                                                        className="form-control"
                                                        placeholder="Saisie nom d'utilisateur"
                                                        type="text"
                                                        onChange={validation.handleChange}
                                                        onBlur={validation.handleBlur}
                                                        value={validation.values.first_name || ""}
                                                        invalid={validation.touched.first_name && !!validation.errors.first_name}
                                                    />
                                                    <FormFeedback type="invalid">{validation.errors.first_name}</FormFeedback>
                                                </div>

                                                <div className="mb-3">
                                                    <Label htmlFor="phone" className="form-label">Numéro de téléphone <span className="text-danger">*</span></Label>
                                                    <Input
                                                        id="phone"
                                                        name="phone"
                                                        className="form-control"
                                                        placeholder="Saisie numéro de téléphone"
                                                        type="text"
                                                        onChange={validation.handleChange}
                                                        onBlur={validation.handleBlur}
                                                        value={validation.values.phone || ""}
                                                        invalid={validation.touched.phone && !!validation.errors.phone}
                                                    />
                                                    <FormFeedback type="invalid">{validation.errors.phone}</FormFeedback>
                                                </div>

                                                <div className="mb-3">
                                                    <Label htmlFor="password" className="form-label">Mot de passe <span className="text-danger">*</span></Label>
                                                    <Input
                                                        id="password"
                                                        name="password"
                                                        className="form-control"
                                                        placeholder="Saisie mot de passe"
                                                        type="password"
                                                        onChange={validation.handleChange}
                                                        onBlur={validation.handleBlur}
                                                        value={validation.values.password || ""}
                                                        invalid={validation.touched.password && !!validation.errors.password}
                                                    />
                                                    <FormFeedback type="invalid">{validation.errors.password}</FormFeedback>
                                                </div>

                                                <div className="mb-3">
                                                    <Label htmlFor="confirm_password" className="form-label">Confirmez Mot de passe <span className="text-danger">*</span></Label>
                                                    <Input
                                                        id="confirm_password"
                                                        name="confirm_password"
                                                        className="form-control"
                                                        placeholder="Confirmez mot de passe"
                                                        type="password"
                                                        onChange={validation.handleChange}
                                                        onBlur={validation.handleBlur}
                                                        value={validation.values.confirm_password || ""}
                                                        invalid={validation.touched.confirm_password && !!validation.errors.confirm_password}
                                                    />
                                                    <FormFeedback type="invalid">{validation.errors.confirm_password}</FormFeedback>
                                                </div>

                                                <div className="mb-4">
                                                    <p className="mb-0 fs-12 text-muted fst-italic">En vous inscrivant, vous acceptez le SPT
                                                        <Link to="#" className="text-primary text-decoration-underline fst-normal fw-medium">Conditions d'utilisation</Link>
                                                    </p>
                                                </div>

                                                <div className="mt-4">
                                                    <Button color="success" type="submit" block>Créer</Button>
                                                </div>

                                            </Form>
                                        </div>
                                    </CardBody>
                                </Card>
                                <div className="mt-4 text-center">
                                    <p className="mb-0">Vous avez déjà un compte ? <Link to="/login" className="fw-semibold text-primary text-decoration-underline">Connectez-vous</Link> </p>
                                </div>
                            </Col>
                        </Row>
                    </Container>
                </div>
            </ParticlesAuth>
        </React.Fragment>
    );
};

export default Register;
