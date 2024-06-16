import { Component } from 'react';
import BookmarkTitle from './BookmarkTitle.jsx';
import BookmarkDomain from './BookmarkDomain.jsx';
import BookmarkDate from './BookmarkDate.jsx';

export default class Bookmark extends Component {
	render() {
		return (
			<div className="bg-gray-100">
				<BookmarkTitle />
				<BookmarkDomain />
				<BookmarkDate />
			</div>
		);
	}    
}