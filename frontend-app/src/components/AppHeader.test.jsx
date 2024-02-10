import { test, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import AppHeader from './AppHeader.jsx';

test('renders App Header', () => {
	render(<AppHeader />);
	const header = screen.getByText(/Bookmarks/i);
	expect(header).not.toBeNull();
});
