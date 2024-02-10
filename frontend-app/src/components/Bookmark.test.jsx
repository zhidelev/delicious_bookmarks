import { test, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Bookmark from './Bookmark.jsx';

test('renders learn react link', () => {
	render(<Bookmark />);
	const linkElement = screen.getByText(/Title/i);
	expect(linkElement).not.toBeNull();
});
