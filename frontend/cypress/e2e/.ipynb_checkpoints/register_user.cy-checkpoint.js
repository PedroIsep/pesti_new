describe('template spec', () => {
  it('passes', () => {
    cy.visit('https://30d24dda-c024-4004-aa5a-497ae648c80a.e1-eu-north-azure.choreoapps.dev/register')
    
    // Confirm that the image is loaded
    cy.get('img').should('be.visible')

    // Fill in the username and password fields
    cy.get('input[placeholder="Username"]').type('testuser')
    cy.get('input[placeholder="Password"]').type('testpassword123')

    // Submit the form
    cy.get('form').submit()

    // Verify that the user is redirected to the login page
    cy.url().should('include', 'e1-eu-north-azure.choreoapps.dev')
  })
})
