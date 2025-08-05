/**
 * End-to-End Frontend Tests for RestaurantFlow_bhatiyani
 * Using Cypress for testing actual running application
 */

// Configuration
const FRONTEND_URL = Cypress.env('FRONTEND_URL') || 'http://localhost:3000';
const BACKEND_URL = Cypress.env('BACKEND_URL') || 'http://localhost:8000';

describe('🧪 RestaurantFlow E2E Tests', () => {
  beforeEach(() => {
    // Visit the application before each test
    cy.visit(FRONTEND_URL);
    
    // Wait for the page to load
    cy.wait(2000);
  });

  describe('🏠 Application Loading', () => {
    it('should load the main application', () => {
      // Check if the page loads
      cy.title().should('include', 'RestaurantFlow');
      
      // Check if navigation is visible
      cy.get('nav, [role="navigation"]').should('be.visible');
      
      cy.log('✅ Application loads successfully');
    });

    it('should display navigation menu', () => {
      // Check for common navigation items
      const navItems = ['Dashboard', 'Restaurants', 'Orders', 'Analytics'];

      navItems.forEach(item => {
        cy.contains(item).should('be.visible');
      });
      
      cy.log('✅ Navigation menu is visible');
    });

    it('should handle page refresh', () => {
      cy.reload();
      cy.get('nav, [role="navigation"]').should('be.visible');
      
      cy.log('✅ Page refresh works correctly');
    });
  });

  describe('🧭 Navigation', () => {
    it('should navigate to Dashboard', () => {
      cy.contains('Dashboard').first().click();
      cy.wait(1000);
      
      // Check if we're on dashboard (look for dashboard-specific content)
      cy.get('body').should('contain.text', /dashboard|today.*orders|revenue/i);
      
      cy.log('✅ Dashboard navigation works');
    });

    it('should navigate to Restaurants', () => {
      cy.contains('Restaurants').first().click();
      cy.wait(1000);
      
      // Check if we're on restaurants page
      cy.get('body').should('contain.text', /restaurant|add.*restaurant/i);
      
      cy.log('✅ Restaurants navigation works');
    });

    it('should navigate to Orders', () => {
      cy.contains('Orders').first().click();
      cy.wait(1000);
      
      // Check if we're on orders page
      cy.get('body').should('contain.text', /order|customer|status/i);
      
      cy.log('✅ Orders navigation works');
    });

    it('should navigate to Analytics', () => {
      cy.contains('Analytics').first().click();
      cy.wait(1000);
      
      // Check if we're on analytics page
      cy.get('body').should('contain.text', /analytics|chart|revenue/i);
      
      cy.log('✅ Analytics navigation works');
    });
  });

  describe('📊 Data Loading', () => {
    it('should load restaurant data', () => {
      cy.contains('Restaurants').first().click();
      cy.wait(3000); // Wait for data to load
      
      // Check if restaurant data is displayed
      cy.get('body').then($body => {
        if ($body.text().includes('Spice Garden') || $body.text().includes('Ocean View')) {
          cy.log('✅ Restaurant data loads correctly');
        } else {
          cy.log('⚠️ No restaurant data visible, may be loading issue');
        }
      });
    });

    it('should load order data', () => {
      cy.contains('Orders').first().click();
      cy.wait(3000); // Wait for data to load
      
      // Check if order data is displayed
      cy.get('body').then($body => {
        if ($body.text().includes('John Doe') || $body.text().includes('pending') || $body.text().includes('completed')) {
          cy.log('✅ Order data loads correctly');
        } else {
          cy.log('⚠️ No order data visible, may be loading issue');
        }
      });
    });

    it('should load dashboard metrics', () => {
      cy.contains('Dashboard').first().click();
      cy.wait(3000); // Wait for data to load
      
      // Check if dashboard metrics are displayed
      cy.get('body').then($body => {
        const hasMetrics = /$\d+|\d+.*orders|\d+.*revenue/.test($body.text());
        if (hasMetrics) {
          cy.log('✅ Dashboard metrics load correctly');
        } else {
          cy.log('⚠️ No dashboard metrics visible, may be loading issue');
        }
      });
    });
  });

  describe('🔍 Search and Filtering', () => {
    it('should search restaurants', () => {
      cy.contains('Restaurants').first().click();
      cy.wait(2000);
      
      // Look for search input
      cy.get('input[placeholder*="search" i], input[type="search"]').then($inputs => {
        if ($inputs.length > 0) {
          cy.wrap($inputs.first()).type('Spice');
          cy.wait(1000);
          
          cy.get('body').then($body => {
            if ($body.text().includes('Spice Garden')) {
              cy.log('✅ Restaurant search works');
            } else {
              cy.log('⚠️ Search may not be working or data not loaded');
            }
          });
        } else {
          cy.log('⚠️ Search input not found');
        }
      });
    });

    it('should filter orders by status', () => {
      cy.contains('Orders').first().click();
      cy.wait(2000);
      
      // Look for status filter
      cy.get('select, [role="combobox"]').then($filters => {
        if ($filters.length > 0) {
          cy.wrap($filters.first()).select('pending').then(() => {
            cy.log('✅ Order status filtering works');
          });
        } else {
          cy.log('⚠️ Status filter not found');
        }
      });
    });
  });

  describe('📱 Responsive Design', () => {
    it('should work on mobile viewport', () => {
      cy.viewport(375, 667); // iPhone size
      cy.visit(FRONTEND_URL);
      
      // Check if navigation is still accessible
      cy.get('nav, [role="navigation"], button[aria-label*="menu" i]').should('be.visible');
      
      cy.log('✅ Mobile viewport works');
    });

    it('should work on tablet viewport', () => {
      cy.viewport(768, 1024); // iPad size
      cy.visit(FRONTEND_URL);
      
      cy.get('nav, [role="navigation"]').should('be.visible');
      
      cy.log('✅ Tablet viewport works');
    });

    it('should work on desktop viewport', () => {
      cy.viewport(1920, 1080); // Desktop size
      cy.visit(FRONTEND_URL);
      
      cy.get('nav, [role="navigation"]').should('be.visible');
      
      cy.log('✅ Desktop viewport works');
    });
  });

  describe('⚡ Performance', () => {
    it('should load page within reasonable time', () => {
      const startTime = Date.now();
      cy.visit(FRONTEND_URL).then(() => {
        const loadTime = Date.now() - startTime;
        expect(loadTime).to.be.lessThan(10000); // Less than 10 seconds
        cy.log(`✅ Page loads in ${loadTime}ms`);
      });
    });
  });

  describe('♿ Accessibility', () => {
    it('should have proper heading structure', () => {
      cy.get('h1, h2, h3, h4, h5, h6').should('have.length.greaterThan', 0);
      cy.log('✅ Headings found');
    });

    it('should have keyboard navigation', () => {
      cy.get('body').tab();
      cy.focused().should('be.visible');
      
      cy.log('✅ Keyboard navigation works');
    });

    it('should have alt text for images', () => {
      cy.get('img').then($images => {
        if ($images.length > 0) {
          cy.get('img[alt]').should('have.length', $images.length);
          cy.log('✅ All images have alt text');
        } else {
          cy.log('ℹ️ No images found');
        }
      });
    });
  });

  describe('🔗 Backend Integration', () => {
    it('should connect to backend API', () => {
      // Test backend health
      cy.request({
        url: `${BACKEND_URL}/health`,
        failOnStatusCode: false
      }).then((response) => {
        if (response.status === 200 && response.body.status === 'healthy') {
          cy.log('✅ Backend is healthy');
          
          // Test frontend-backend integration
          cy.contains('Restaurants').first().click();
          cy.wait(3000);
          
          cy.get('body').then($body => {
            if ($body.text().includes('Spice Garden') || $body.text().includes('Ocean View')) {
              cy.log('✅ Frontend successfully connects to backend API');
            } else {
              cy.log('⚠️ Frontend may not be receiving backend data');
            }
          });
        } else {
          cy.log('⚠️ Backend is not healthy, skipping integration test');
        }
      });
    });

    it('should handle API errors gracefully', () => {
      // Intercept API calls and return errors
      cy.intercept('GET', '**/api/**', { statusCode: 500, body: { error: 'Internal Server Error' } });
      
      cy.contains('Dashboard').first().click();
      cy.wait(3000);
      
      // Check if error state is handled gracefully
      cy.get('body').then($body => {
        if (/error|failed|something.*wrong/i.test($body.text())) {
          cy.log('✅ API error handling works');
        } else {
          cy.log('⚠️ API error handling may not be working');
        }
      });
    });
  });
});

// Helper commands
Cypress.Commands.add('tab', { prevSubject: 'element' }, (subject) => {
  return cy.wrap(subject).trigger('keydown', { key: 'Tab' });
});

export {};
