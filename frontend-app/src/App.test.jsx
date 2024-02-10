import { test, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';

test('app has header part', () => {
	render(<App />);
	const header = screen.getByText(/Bookmarks/i);
	expect(header).not.toBeNull();
});

test('app has footer part', () => {
	const footer = screen.getByText(/Footer/i);
	expect(footer).not.toBeNull();
});
