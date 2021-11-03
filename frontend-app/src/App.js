import './App.css';
import Link from './components/Link';
import AppHeader from './components/AppHeader';
import React, { Component } from 'react';
import AppFooter from './components/AppFooter';

export default class App extends Component {

  render() {
    return (
      <div>
        <AppHeader />
        Hello, world
        <Link />
        <AppFooter />
      </div>
    );
  } 
};
