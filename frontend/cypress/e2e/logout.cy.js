describe('template spec', () => {
  it('passes', () => {
    cy.visit('localhost:5173/login')
      
    cy.get('img')

    // Fill in the username and password fields
    cy.get('input[placeholder="Username"]').type('testuser')
    cy.get('input[placeholder="Password"]').type('testpassword123')
        
    // Submit the form
    cy.get('form').submit()
    
    // Logout button
    cy.get('a').contains("Logout").click()

    cy.url().should('include', 'localhost:5173/login')
  })
})
  