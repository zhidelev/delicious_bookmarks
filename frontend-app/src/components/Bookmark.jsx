import { Component } from 'react';
import BookmarkTitle from './BookmarkTitle.jsx';
import BookmarkDomain from './BookmarkDomain.jsx';
import BookmarkDate from './BookmarkDate.jsx';

export default class Bookmark extends Component {
	render() {
		return (
			<div className="relative auto-rows-max border-2 rounded-br-lg border-l-indigo-50 shadow-lg w-1/2">
				<BookmarkTitle />
				<BookmarkDomain />
				<BookmarkDate />
			</div>
		);
	}    
}