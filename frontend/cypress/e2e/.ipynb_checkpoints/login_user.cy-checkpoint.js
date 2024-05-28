describe('template spec', () => {
  it('passes', () => {
    cy.visit('localhost:5173/login')
  

    // Fill in the username and password fields
    cy.get('input[placeholder="Username"]').type('testuser')
    cy.get('input[placeholder="Password"]').type('testpassword123')
    
    // Submit the form
    cy.get('form').submit()
    
    // Verify that the user is redirected to the login page
    cy.url().should('include', 'localhost:5173')
  })
})