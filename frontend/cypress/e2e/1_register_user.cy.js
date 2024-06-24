describe('template spec', () => {
  it('passes', () => {
    cy.visit('https://9f9683d8-14d0-4581-b2f7-393d1ea2e5b2.e1-eu-north-azure.choreoapps.dev/register')
    
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
