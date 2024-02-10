import './App.css';
import Bookmark from './components/Bookmark';
import AppHeader from './components/AppHeader';
import { Component } from 'react';
import AppFooter from './components/AppFooter';

export default class App extends Component {

	render() {
		return (
			<div className="m-8 grid justify-items-center">
				<AppHeader />
				<Bookmark />
				<AppFooter />
			</div>
		);
	} 
}
