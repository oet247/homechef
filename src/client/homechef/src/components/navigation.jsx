import Nav from 'react-bootstrap/Nav';
import React, { useState, useEffect} from 'react';
import './navigation.css'


export function Navigation() {

     const [isAuth, setIsAuth] = useState(false);

      useEffect(() => {
           if (localStorage.getItem('access_token') !== null) {
                    setIsAuth(true); 
        }
      }, [isAuth]);
      
      return ( 
        <div className='navBar'>           
            <Nav className='home'> 
            <Nav.Link className='navText' href="/">HOME</Nav.Link>
            </Nav>
            <div className='form'>
              <Nav className='navBox'>
                {isAuth ? <Nav.Link className='navText' href="/profilepage">PROFILE PAGE</Nav.Link> : null}
              </Nav>
              <Nav className='navBox'>
              {isAuth ? <Nav.Link className='navText' href="/logout">LOG OUT</Nav.Link> : <Nav.Link className='navText' href="/login">LOGIN</Nav.Link>}
              </Nav>
              <Nav className='navBox'>
                {!isAuth ? <Nav.Link className='navText' href="/registration">REGISTER</Nav.Link> : null}
              </Nav>
            </div>
        </div>
      );
}