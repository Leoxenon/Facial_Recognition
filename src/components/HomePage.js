import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/main.css';

const HomePage = () => {
    return (
        <div className="container">
            <div className="card">
                <h2>Welcome to Face Recognition Auth</h2>
                <div className="button-group">
                    <Link to="/login" className="btn btn-primary">
                        Login
                    </Link>
                    <Link to="/register" className="btn btn-primary">
                        Register
                    </Link>
                    <Link to="/password-recovery" className="btn btn-secondary">
                        Forgot Password?
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default HomePage; 