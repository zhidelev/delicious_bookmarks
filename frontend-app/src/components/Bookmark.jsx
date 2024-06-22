import BookmarkTitle from './BookmarkTitle.jsx';
import BookmarkDomain from './BookmarkDomain.jsx';
import BookmarkDate from './BookmarkDate.jsx';

function Bookmark(){
	
	return (
		<div>
			<BookmarkTitle />
			<BookmarkDomain />
			<BookmarkDate />
			<h1 className="text-3xl font-bold underline">
    Hello world!
			</h1>
		</div>
	);
  
}

export default Bookmark;