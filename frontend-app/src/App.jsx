import './App.css';
import Bookmark from './components/Bookmark';
import AppHeader from './components/AppHeader';
import AppFooter from './components/AppFooter';
import BookmarksList from './components/BookmarksList';

function App() {
	const data = [
		{'id': 1, 'title': 'Title 1', 'domain': 'Domain 1', 'date': '2021-01-01'},
		{'id': 2, 'title': 'Title 2', 'domain': 'Domain 2', 'date': '2021-01-02'}
	];

	
	return (
		<div className="m-8 grid justify-items-center">
			<AppHeader />
			<BookmarksList>
				{data.map(el => (
					<Bookmark key={el.id} />
					
				))}
			</BookmarksList>
				
			<AppFooter />
		</div>
	);
	
}

export default App;