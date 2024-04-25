import React, { useState } from 'react';
import {
    Col,
    Row,
    Button,
    UncontrolledDropdown,
    DropdownToggle,
    DropdownItem,
    DropdownMenu,
} from "reactstrap";
import { Link } from "react-router-dom";
import Flatpickr from "react-flatpickr";
import Select from "react-select";


const CustomersGlobalFilter = () => {
    const [customerStatus, setcustomerStatus] = useState(null);

    function handlecustomerStatus(customerStatus) {
        setcustomerStatus(customerStatus);
    }

    const customerstatus = [
        {
            options: [
                { label: "Status", value: "Status" },
                { label: "All", value: "All" },
                { label: "Active", value: "Active" },
                { label: "Block", value: "Block" },
            ],
        },
    ];
    return (
        <React.Fragment>
            <Col xl={7}>
                <Row className="g-3">
                    <Col sm={4}>
                        <div className="">
                            <Flatpickr
                                className="form-control"
                                id="datepicker-publish-input"
                                placeholder="Select a date"
                                options={{
                                    altInput: true,
                                    altFormat: "F j, Y",
                                    mode: "multiple",
                                    dateFormat: "d.m.y",
                                }}
                            />
                        </div>
                    </Col>

                    <Col sm={4}>
                        <div>
                            <Select
                                value={customerStatus}
                                onChange={(e) => {
                                    handlecustomerStatus(e.value);
                                }}
                                options={customerstatus}
                                name="choices-single-default"
                                id="idStatus"
                            ></Select>
                        </div>
                    </Col>

                    <Col sm={4}>
                        <div>
                            <button
                                type="button"
                                className="btn btn-primary w-100"
                            >
                                {" "}
                                <i className="ri-equalizer-fill me-2 align-bottom"></i>
                                Filtres
                            </button>
                        </div>
                    </Col>
                </Row>
            </Col>
        </React.Fragment>
    );
};

const OrderGlobalFilter = () => {
    const [orderStatus, setorderStatus] = useState([]);
    const [orderPayement, setorderPayement] = useState(null);

    function handleorderStatus(orderstatus) {
        setorderStatus(orderstatus);
    }

    function handleorderPayement(orderPayement) {
        setorderPayement(orderPayement);
    }

    const orderstatus = [
        {
            options: [
                { label: "Status", value: "Status" },
                { label: "All", value: "All" },
                { label: "Pending", value: "Pending" },
                { label: "Inprogress", value: "Inprogress" },
                { label: "Cancelled", value: "Cancelled" },
                { label: "Pickups", value: "Pickups" },
                { label: "Returns", value: "Returns" },
                { label: "Delivered", value: "Delivered" },
            ],
        },
    ];

    const orderpayement = [
        {
            options: [
                { label: "Select Payment", value: "Select Payment" },
                { label: "All", value: "All" },
                { label: "Mastercard", value: "Mastercard" },
                { label: "Paypal", value: "Paypal" },
                { label: "Visa", value: "Visa" },
                { label: "COD", value: "COD" },
            ],
        },
    ];
    return (
        <React.Fragment>
            <Col sm={6} className="col-xxl-2">
                <div>
                    <Flatpickr
                        className="form-control"
                        id="datepicker-publish-input"
                        placeholder="Select a date"
                        options={{
                            altInput: true,
                            altFormat: "F j, Y",
                            mode: "multiple",
                            dateFormat: "d.m.y",
                        }}
                    />
                </div>
            </Col>

            <Col sm={4} className="col-xxl-2">
                <div>
                    <Select
                        value={orderStatus}
                        onChange={(e) => {
                            handleorderStatus(e);
                        }}
                        options={orderstatus}
                        name="choices-single-default"
                        id="idStatus"
                    ></Select>
                </div>
            </Col>

            <Col sm={4} className="col-xxl-2">
                <div>
                    <Select
                        value={orderPayement}
                        onChange={() => {
                            handleorderPayement();
                        }}
                        options={orderpayement}
                        name="choices-payment-default"
                        id="idPayment"
                    ></Select>
                </div>
            </Col>

            <Col sm={4} className="col-xxl-1">
                <div>
                    <button type="button" className="btn btn-primary w-100">
                        {" "}
                        <i className="ri-equalizer-fill me-1 align-bottom"></i>
                        Filtres
                    </button>
                </div>
            </Col>
        </React.Fragment>
    );
};

const ContactsGlobalFilter = () => {
    const [sortBy, setsortBy] = useState(null);

    function handlesortBy(sortBy) {
        setsortBy(sortBy);
    }

    const sortbyname = [
        {
            options: [
                { label: "Owner", value: "Owner" },
                { label: "Company", value: "Company" },
                { label: "Location", value: "Location" }
            ],
        },
    ];
    return (
        <React.Fragment>
            <div className="col-md-auto ms-auto">
                <div className="d-flex align-items-center gap-2">
                    <span className="text-muted">Trier par : </span>
                    <Select
                        className="mb-0"
                        value={sortBy}
                        onChange={() => {
                            handlesortBy();
                        }}
                        options={sortbyname}
                        id="choices-single-default"
                    >
                    </Select>
                </div>
            </div>
        </React.Fragment>
    );
};



const InvoiceListGlobalSearch = () => {
    const [isStatus, setisStatus] = useState(null);


    function handleisStatus(isStatus) {
        setisStatus(isStatus);
    }

    const allstatus = [
        {
            options: [
                { label: "Status", value: "Status" },
                { label: "All", value: "All" },
                { label: "Unpaid", value: "Unpaid" },
                { label: "Paid", value: "Paid" },
                { label: "Cancel", value: "Cancel" },
                { label: "Refund", value: "Refund" },
            ],
        },
    ];
    return (
        <React.Fragment>
            <Col sm={4} xxl={3}>
                <Flatpickr
                    className="form-control bg-light border-light"
                    id="datepicker-publish-input"
                    placeholder="Select a date"
                    options={{
                        altInput: true,
                        altFormat: "F j, Y",
                        mode: "multiple",
                        dateFormat: "d.m.y",
                    }}
                />
            </Col>

            <Col sm={4} xxl={3}>
                <div className="input-light">
                    <Select
                        value={isStatus}
                        onChange={() => {
                            handleisStatus();
                        }}
                        options={allstatus}
                        name="choices-single-default"
                        id="idStatus"
                    ></Select>
                </div>
            </Col>

            <Col sm={4} xxl={1}>
                <Button color="primary" className="w-100">
                    <i className="ri-equalizer-fill me-1 align-bottom"></i>{" "}
                    Filtres
                </Button>
            </Col>

        </React.Fragment>
    );
};


const NFTRankingGlobalFilter = () => {
    return (
        <React.Fragment>
            <Col xxl={2} sm={4} className="ms-auto">
                <div>
                    <select className="form-control" data-choices data-choices-search-false name="choices-single-default" id="idStatus">
                        <option value="All Time" defaultValue>All Time</option>
                        <option value="1 Day">1 Day</option>
                        <option value="7 Days">7 Days</option>
                        <option value="15 Days">15 Days</option>
                        <option value="1 Month">1 Month</option>
                        <option value="6 Month">6 Month</option>
                    </select>
                </div>
            </Col>
        </React.Fragment>
    );
};



export {
   
    CustomersGlobalFilter,
    OrderGlobalFilter,
    ContactsGlobalFilter,
    
    InvoiceListGlobalSearch,
    
    NFTRankingGlobalFilter
   
};