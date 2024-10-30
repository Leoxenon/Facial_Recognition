import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import HomePage from './components/HomePage';
import AuthenticationPage from './components/AuthenticationPage';
import RegisterPage from './components/RegisterPage';
import PasswordRecoveryPage from './components/PasswordRecoveryPage';
import './styles/main.css';

function App() {
    return (
        <Router>
            <Switch>
                <Route exact path="/" component={HomePage} />
                <Route path="/login" component={AuthenticationPage} />
                <Route path="/register" component={RegisterPage} />
                <Route path="/password-recovery" component={PasswordRecoveryPage} />
            </Switch>
        </Router>
    );
}

export default App;
