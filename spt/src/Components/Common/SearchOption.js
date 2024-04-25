import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Input } from 'reactstrap';

//SimpleBar
import SimpleBar from "simplebar-react";

//import images
import image2 from "../../assets/images/users/avatar-2.jpg";
import image3 from "../../assets/images/users/avatar-3.jpg";
import image5 from "../../assets/images/users/avatar-5.jpg";

const SearchOption = () => {
    const [value, setValue] = useState("");
    const onChangeData = (value) => {
        setValue(value);
    };

    useEffect(() => {
        var searchOptions = document.getElementById("search-close-options");
        var dropdown = document.getElementById("search-dropdown");
        var searchInput = document.getElementById("search-options");

        searchInput.addEventListener("focus", function () {
            var inputLength = searchInput.value.length;
            if (inputLength > 0) {
                dropdown.classList.add("show");
                searchOptions.classList.remove("d-none");
            } else {
                dropdown.classList.remove("show");
                searchOptions.classList.add("d-none");
            }
        });

        searchInput.addEventListener("keyup", function () {
            var inputLength = searchInput.value.length;
            if (inputLength > 0) {
                dropdown.classList.add("show");
                searchOptions.classList.remove("d-none");
            } else {
                dropdown.classList.remove("show");
                searchOptions.classList.add("d-none");
            }
        });

        searchOptions.addEventListener("click", function () {
            searchInput.value = "";
            dropdown.classList.remove("show");
            searchOptions.classList.add("d-none");
        });

        document.body.addEventListener("click", function (e) {
            if (e.target.getAttribute('id') !== "search-options") {
                dropdown.classList.remove("show");
                searchOptions.classList.add("d-none");
            }
        });
    }, []);

    return (
        <React.Fragment>
            <form className="app-search d-none d-md-block">
                <div className="position-relative">
                    <Input type="text" className="form-control" placeholder="Chercher..."
                        id="search-options"
                        value={value}
                        onChange={e => {
                            onChangeData(e.target.value);
                        }} />
                    <span className="mdi mdi-magnify search-widget-icon"></span>
                    <span className="mdi mdi-close-circle search-widget-icon search-widget-icon-close d-none"
                        id="search-close-options"></span>
                </div>
                <div className="dropdown-menu dropdown-menu-lg" id="search-dropdown">
                    <SimpleBar style={{ height: "320px" }}>

                        <div className="dropdown-header">
                            <h6 className="text-overflow text-muted mb-0 text-uppercase">Recherches récentes</h6>
                        </div>

                        
                        <div className="dropdown-header mt-2">
                            <h6 className="text-overflow text-muted mb-1 text-uppercase">Pages</h6>
                        </div>


                       


                        

                        <Link to="#" className="dropdown-item notify-item">
                            <i className="ri-user-settings-line align-middle fs-18 text-muted me-2"></i>
                            <span>Mes paramètres de compte</span>
                        </Link>


                        
                       
                        
                    </SimpleBar>

                    <div className="text-center pt-3 pb-1">
                        <Link to="/pages-search-results" className="btn btn-primary btn-sm">Voir tous les résultats <i
                            className="ri-arrow-right-line ms-1"></i></Link>
                    </div>
                </div>
            </form>
        </React.Fragment>
    );
};

export default SearchOption;