import { test, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import AppFooter from './AppFooter.jsx';

test('renders App Footer', () => {
	render(<AppFooter />);
	const footer = screen.getByText(/Footer/i);
	expect(footer).not.toBeNull();
});