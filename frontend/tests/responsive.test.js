// Test responsive behavior across multiple screen sizes
describe('Responsive Behavior Tests', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  it('should render correctly on mobile screens (375px)', () => {
    cy.viewport(375, 667); // iPhone SE size
    cy.get('header').should('be.visible');
    cy.get('.task-form').should('have.css', 'padding', '16px'); // 1rem
    cy.get('.task-item').should('have.css', 'margin-bottom', '16px');

    // Check if mobile-specific classes are applied
    cy.get('.mobile-header').should('exist');
    cy.get('.welcome-text').should('not.be.visible');
    cy.get('.mobile-welcome').should('be.visible');
  });

  it('should render correctly on tablet screens (768px)', () => {
    cy.viewport(768, 1024); // iPad size
    cy.get('header').should('be.visible');
    cy.get('.stats-grid').should('have.css', 'grid-template-columns', 'repeat(2, 1fr)');
    cy.get('.task-list-section').should('have.css', 'padding', '24px'); // 1.5rem
  });

  it('should render correctly on desktop screens (1200px)', () => {
    cy.viewport(1200, 800);
    cy.get('header').should('be.visible');
    cy.get('.stats-grid').should('have.css', 'grid-template-columns', 'repeat(3, 1fr)');
  });

  it('should handle orientation changes properly', () => {
    cy.viewport(1024, 768); // Desktop in portrait
    cy.get('.stats-grid').should('have.css', 'grid-template-columns', 'repeat(2, 1fr)');

    cy.viewport(1024, 1366); // Desktop in landscape
    cy.get('.stats-grid').should('have.css', 'grid-template-columns', 'repeat(2, 1fr)');
  });

  it('should maintain accessibility features across screen sizes', () => {
    cy.viewport(375, 667); // Mobile
    cy.get('button').each(($btn) => {
      cy.wrap($btn).should('have.css', 'min-height').and('match', /44px/);
    });

    cy.get('input').each(($input) => {
      cy.wrap($input).should('have.css', 'min-height').and('match', /40px/);
    });
  });
});