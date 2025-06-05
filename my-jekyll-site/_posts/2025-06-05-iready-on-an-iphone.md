---
layout: very_nice
title: "iReady on iPhone: A Technical Journey from Chromebook to iOS"
date: 2025-06-05
---

<img src="https://i.imgur.com/i0nXXSW.jpeg" style="width: 400px;" alt=""/>

## Introduction {#introduction}

This is the story of reverse-engineering a Chromebook-only educational app to work on iOS Safari. iReady, a popular K-12 learning platform, was deliberately designed to run exclusively on Chromebooks and desktop browsers. Through months of trial-and-error development, we successfully bypassed platform restrictions and adapted the entire application for iPhone and iPad use.

This technical deep-dive chronicles the browser compatibility challenges, mobile web development hurdles, and platform-specific workarounds required to transform a desktop-first application into a functional mobile experience.

## Chapter 1: Breaking Through Platform Detection {#platform-detection}

The first hurdle was iReady's aggressive platform detection system. The application immediately blocked iOS devices, displaying error messages that the platform was "not supported." Our initial approach involved sophisticated user-agent spoofing, mimicking Firefox on macOS with custom navigator object overrides.

We discovered that iReady performed deep browser fingerprinting, checking not just the user-agent string but also navigator.platform, navigator.vendor, screen dimensions, and the presence of touch APIs. The solution required comprehensive JavaScript injection to replace these properties before the iReady scripts could execute.

```javascript
// Complete navigator object spoofing for desktop Firefox on macOS
function spoofNavigator() {
    const originalNavigator = window.navigator;
    
    // Create fake navigator properties
    const fakeNavigator = {
        userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
        platform: 'MacIntel',
        vendor: '',
        appVersion: '5.0 (Macintosh)',
        appName: 'Netscape',
        product: 'Gecko',
        maxTouchPoints: 0,
        hardwareConcurrency: 8,
        deviceMemory: 8,
        webdriver: undefined
    };
    
    // Override navigator properties before page scripts load
    Object.defineProperty(window, 'navigator', {
        value: new Proxy(originalNavigator, {
            get(target, prop) {
                return fakeNavigator.hasOwnProperty(prop) 
                    ? fakeNavigator[prop] 
                    : target[prop];
            }
        }),
        writable: false,
        configurable: false
    });
    
    // Remove touch-related APIs entirely
    delete window.Touch;
    delete window.TouchEvent;
    delete window.TouchList;
    
    console.log('Navigator spoofing complete:', window.navigator.userAgent);
}

// Execute immediately before any other scripts
spoofNavigator();
```

<div style="background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 20px; margin: 20px 0;">
    <h4 style="color: #495057; margin-top: 0;">Platform Detection Bypass Results</h4>
    <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
        <div style="background: #dc3545; color: white; padding: 8px 12px; border-radius: 4px; flex: 1; margin-right: 10px; text-align: center;">
            <strong>Before:</strong><br>
            "iOS not supported"
        </div>
        <div style="background: #28a745; color: white; padding: 8px 12px; border-radius: 4px; flex: 1; text-align: center;">
            <strong>After:</strong><br>
            "Welcome to iReady"
        </div>
    </div>
    <small style="color: #6c757d;">Detection methods bypassed: User-agent, platform, vendor, touch APIs, screen dimensions</small>
</div>

## Chapter 2: Conquering OAuth and Authentication Flows {#authentication-flows}

iReady's authentication system relies on Clever SSO, creating a complex multi-domain authentication flow. iOS WebView's strict cookie and session handling broke this process completely. We had to implement custom cookie injection, hardcoding authentication tokens and maintaining session state across domain redirects.

The challenge intensified when we discovered that Clever's OAuth implementation expected specific HTTP headers that mobile Safari didn't provide. Our solution involved intercepting and modifying network requests to inject the necessary authentication headers.

<div style="background: #f8f9fa; border: 2px solid #dee2e6; border-radius: 12px; padding: 25px; margin: 25px 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
    <h4 style="text-align: center; color: #495057; margin-bottom: 25px; font-size: 18px;">Multi-Domain Authentication Flow</h4>
    
    <div style="display: flex; flex-direction: column; gap: 15px;">
        <!-- Step 1 -->
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="background: #007bff; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0;">1</div>
            <div style="background: #e3f2fd; padding: 12px 16px; border-radius: 8px; flex: 1; border-left: 4px solid #2196f3;">
                <strong>school.iready.com</strong><br>
                <small style="color: #666;">Initial login attempt → Redirect to Clever SSO</small>
            </div>
        </div>
        
        <!-- Arrow -->
        <div style="text-align: center; color: #666; font-size: 20px;">↓</div>
        
        <!-- Step 2 -->
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="background: #28a745; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0;">2</div>
            <div style="background: #e8f5e8; padding: 12px 16px; border-radius: 8px; flex: 1; border-left: 4px solid #4caf50;">
                <strong>clever.com/oauth/authorize</strong><br>
                <small style="color: #666;">OAuth authorization with district credentials</small>
            </div>
        </div>
        
        <!-- Arrow -->
        <div style="text-align: center; color: #666; font-size: 20px;">↓</div>
        
        <!-- Step 3 -->
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="background: #ffc107; color: black; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0;">3</div>
            <div style="background: #fff8e1; padding: 12px 16px; border-radius: 8px; flex: 1; border-left: 4px solid #ff9800;">
                <strong>clever.com/oauth/tokens</strong><br>
                <small style="color: #666;">Token exchange with authorization code</small>
            </div>
        </div>
        
        <!-- Arrow -->
        <div style="text-align: center; color: #666; font-size: 20px;">↓</div>
        
        <!-- Step 4 -->
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="background: #dc3545; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0;">4</div>
            <div style="background: #ffebee; padding: 12px 16px; border-radius: 8px; flex: 1; border-left: 4px solid #f44336;">
                <strong>login.iready.com/sso/clever</strong><br>
                <small style="color: #666;">Final authentication with session cookies</small>
            </div>
        </div>
    </div>
    
    <div style="margin-top: 20px; padding: 15px; background: #fff3cd; border-left: 4px solid #ffc107; border-radius: 0 8px 8px 0;">
        <strong style="color: #856404;">⚠️ iOS WebView Issues:</strong><br>
        <small style="color: #856404;">• Cookies lost between domains<br>• Missing Authorization headers<br>• SameSite cookie restrictions</small>
    </div>
</div>

```javascript
// Authentication flow handler with cookie injection
class AuthenticationManager {
    constructor() {
        this.cookies = new Map();
        this.authHeaders = new Map();
        this.setupInterceptors();
    }
    
    setupInterceptors() {
        // Intercept all fetch requests to inject auth headers
        const originalFetch = window.fetch;
        window.fetch = async (url, options = {}) => {
            const domain = new URL(url).hostname;
            
            // Inject required headers based on domain
            const headers = new Headers(options.headers);
            
            if (domain.includes('clever.com')) {
                headers.set('X-Requested-With', 'XMLHttpRequest');
                headers.set('Accept', 'application/json');
                // Inject stored OAuth token
                if (this.authHeaders.has('clever_token')) {
                    headers.set('Authorization', `Bearer ${this.authHeaders.get('clever_token')}`);
                }
            }
            
            if (domain.includes('iready.com')) {
                // Inject session cookies manually
                const sessionCookies = this.getCookiesForDomain('iready.com');
                if (sessionCookies) {
                    headers.set('Cookie', sessionCookies);
                }
                headers.set('X-CSRF-Token', this.getCSRFToken());
            }
            
            return originalFetch(url, { ...options, headers });
        };
    }
    
    // Hardcode authentication tokens from successful desktop login
    injectAuthenticationTokens() {
        // These tokens captured from working desktop session
        this.cookies.set('clever.com', {
            'clever_session': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
            'clever_remember_token': 'abc123def456...'
        });
        
        this.cookies.set('iready.com', {
            'JSESSIONID': 'F8B2C4D6E8A0B2C4...',
            'iready_session': 'user_123_district_456...',
            'csrf_token': 'a1b2c3d4e5f6...'
        });
        
        console.log('Authentication tokens injected successfully');
    }
    
    getCookiesForDomain(domain) {
        const domainCookies = this.cookies.get(domain);
        if (!domainCookies) return null;
        
        return Object.entries(domainCookies)
            .map(([key, value]) => `${key}=${value}`)
            .join('; ');
    }
    
    getCSRFToken() {
        const ireadyCookies = this.cookies.get('iready.com');
        return ireadyCookies?.csrf_token || '';
    }
}

// Initialize authentication manager
const authManager = new AuthenticationManager();
authManager.injectAuthenticationTokens();
```

## Chapter 3: Solving Viewport and Scaling Nightmares {#viewport-scaling}

Perhaps the most visually dramatic issue was iOS WebView's zoom behavior. iReady lessons appeared microscopically small, with students only able to see tiny fragments of the interface. The desktop-designed content expected a 1920x1080 viewport but was being crammed into a 375x667 iPhone screen.

Our fix involved multiple approaches: viewport meta tag manipulation, CSS zoom property adjustments, and WKWebView configuration to set minimum zoom scales. We implemented automatic zoom detection and correction, ensuring content remained readable while preserving layout integrity.

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 25px; margin: 25px 0; color: white;">
    <h4 style="text-align: center; margin-bottom: 25px; color: white;">Viewport Scaling Problem Visualization</h4>
    
    <div style="display: flex; justify-content: space-around; align-items: center; gap: 20px; margin-bottom: 20px;">
        <!-- Desktop Expected -->
        <div style="text-align: center;">
            <div style="background: #34495e; border: 3px solid #ecf0f1; border-radius: 8px; padding: 15px; width: 120px; height: 80px; position: relative; margin: 0 auto;">
                <div style="background: #3498db; width: 100%; height: 100%; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 10px;">
                    iReady Content<br>1920×1080
                </div>
            </div>
            <small style="margin-top: 8px; display: block;">Desktop (Expected)</small>
        </div>
        
        <!-- Arrow -->
        <div style="font-size: 24px; color: #f39c12;">→</div>
        
        <!-- iPhone Reality -->
        <div style="text-align: center;">
            <div style="background: #2c3e50; border: 3px solid #ecf0f1; border-radius: 12px; padding: 8px; width: 60px; height: 100px; position: relative; margin: 0 auto;">
                <div style="background: #e74c3c; width: 100%; height: 100%; border-radius: 4px; overflow: hidden; position: relative;">
                    <div style="background: #3498db; width: 300%; height: 300%; position: absolute; top: -100%; left: -100%; display: flex; align-items: center; justify-content: center; font-size: 6px; transform: scale(0.3);">
                        iReady Content<br>375×667
                    </div>
                </div>
            </div>
            <small style="margin-top: 8px; display: block;">iPhone (Problem)</small>
        </div>
        
        <!-- Arrow -->
        <div style="font-size: 24px; color: #27ae60;">→</div>
        
        <!-- Fixed Solution -->
        <div style="text-align: center;">
            <div style="background: #27ae60; border: 3px solid #ecf0f1; border-radius: 12px; padding: 8px; width: 60px; height: 100px; position: relative; margin: 0 auto;">
                <div style="background: #2ecc71; width: 100%; height: 100%; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-size: 8px;">
                    iReady Content<br>Scaled & Usable
                </div>
            </div>
            <small style="margin-top: 8px; display: block;">iPhone (Fixed)</small>
        </div>
    </div>
    
    <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 20px;">
        <strong>Key Issues Solved:</strong><br>
        • Content appearing at ~20% original size<br>
        • Interactive elements becoming untouchable<br>
        • Text becoming unreadable due to scaling
    </div>
</div>

```javascript
// Comprehensive viewport and scaling solution
class ViewportManager {
    constructor() {
        this.originalViewport = null;
        this.targetScale = 0.7; // Optimal scale for iPhone
        this.setupViewportControl();
        this.monitorZoomChanges();
    }
    
    setupViewportControl() {
        // Remove existing viewport meta tag
        const existingViewport = document.querySelector('meta[name="viewport"]');
        if (existingViewport) {
            this.originalViewport = existingViewport.content;
            existingViewport.remove();
        }
        
        // Inject custom viewport configuration
        const viewportMeta = document.createElement('meta');
        viewportMeta.name = 'viewport';
        viewportMeta.content = `
            width=1200,
            initial-scale=${this.targetScale},
            minimum-scale=0.1,
            maximum-scale=3.0,
            user-scalable=yes,
            viewport-fit=cover
        `.replace(/\s+/g, ' ').trim();
        
        document.head.appendChild(viewportMeta);
        
        console.log('Viewport configured:', viewportMeta.content);
    }
    
    // Override window dimensions to fool desktop-expecting scripts
    spoofWindowDimensions() {
        const fakeWidth = 1920;
        const fakeHeight = 1080;
        
        // Override screen object
        Object.defineProperties(window.screen, {
            width: { value: fakeWidth, writable: false },
            height: { value: fakeHeight, writable: false },
            availWidth: { value: fakeWidth, writable: false },
            availHeight: { value: fakeHeight - 80, writable: false } // Account for browser chrome
        });
        
        // Override window dimensions
        Object.defineProperties(window, {
            innerWidth: { value: fakeWidth, writable: false },
            innerHeight: { value: fakeHeight, writable: false },
            outerWidth: { value: fakeWidth, writable: false },
            outerHeight: { value: fakeHeight, writable: false }
        });
        
        // Override CSS media queries
        this.overrideMediaQueries();
    }
    
    overrideMediaQueries() {
        // Intercept matchMedia to return desktop results
        const originalMatchMedia = window.matchMedia;
        window.matchMedia = (query) => {
            // Force desktop-like responses for common mobile queries
            if (query.includes('max-width: 768px') || 
                query.includes('max-width: 1024px')) {
                return { matches: false, media: query };
            }
            
            if (query.includes('min-width: 1200px') || 
                query.includes('min-width: 1920px')) {
                return { matches: true, media: query };
            }
            
            return originalMatchMedia.call(window, query);
        };
    }
    
    monitorZoomChanges() {
        // Detect when content becomes too small and auto-correct
        const observer = new ResizeObserver((entries) => {
            for (const entry of entries) {
                const contentRect = entry.contentRect;
                if (contentRect.width < 300) { // Content too small
                    this.forceReasonableScale();
                }
            }
        });
        
        // Monitor the main content container
        const contentContainer = document.querySelector('#main-content, .lesson-container, body');
        if (contentContainer) {
            observer.observe(contentContainer);
        }
    }
    
    forceReasonableScale() {
        // Apply CSS transform scaling as fallback
        const body = document.body;
        if (body) {
            body.style.transform = `scale(${this.targetScale})`;
            body.style.transformOrigin = 'top left';
            body.style.width = `${100 / this.targetScale}%`;
            body.style.height = `${100 / this.targetScale}%`;
            
            console.log('Applied emergency scaling:', this.targetScale);
        }
    }
    
    // WKWebView configuration (called from native iOS code)
    configureWebView() {
        // This would be called from Swift/Objective-C
        return {
            minimumZoomScale: 0.1,
            maximumZoomScale: 3.0,
            zoomScale: this.targetScale,
            contentInsetAdjustmentBehavior: 'never',
            scrollView: {
                bounces: false,
                showsVerticalScrollIndicator: true,
                showsHorizontalScrollIndicator: true
            }
        };
    }
}

// Initialize viewport manager immediately
const viewportManager = new ViewportManager();
viewportManager.spoofWindowDimensions();

// Re-run on dynamic content changes
document.addEventListener('DOMContentLoaded', () => {
    viewportManager.setupViewportControl();
});
```

## Chapter 4: Touch Events and Interactive Element Failures {#touch-events}

iReady's interactive elements - draggable light bulbs, clickable math problems, drawing tools - were built exclusively for mouse input. iOS touch events simply didn't register with the desktop-oriented JavaScript event handlers.

We developed comprehensive touch-to-mouse event polyfills, converting touchstart/touchmove/touchend events into their mouse equivalents. Special handling was required for drag-and-drop operations, where we had to prevent iOS's default touch behaviors while maintaining the precision needed for educational interactions.

```javascript
// Comprehensive touch-to-mouse event polyfill system
class TouchEventPolyfill {
    constructor() {
        this.activeTouches = new Map();
        this.dragThreshold = 10; // pixels
        this.touchStartTime = 0;
        this.lastTouchPosition = { x: 0, y: 0 };
        this.setupEventListeners();
        this.preventDefaultBehaviors();
    }
    
    setupEventListeners() {
        // Attach to document to catch all touch events
        document.addEventListener('touchstart', this.handleTouchStart.bind(this), { passive: false });
        document.addEventListener('touchmove', this.handleTouchMove.bind(this), { passive: false });
        document.addEventListener('touchend', this.handleTouchEnd.bind(this), { passive: false });
        document.addEventListener('touchcancel', this.handleTouchCancel.bind(this), { passive: false });
        
        console.log('Touch event polyfill initialized');
    }
    
    preventDefaultBehaviors() {
        // Prevent iOS default behaviors that interfere with drag operations
        document.addEventListener('gesturestart', (e) => e.preventDefault(), { passive: false });
        document.addEventListener('gesturechange', (e) => e.preventDefault(), { passive: false });
        document.addEventListener('gestureend', (e) => e.preventDefault(), { passive: false });
        
        // Prevent text selection during drags
        document.addEventListener('selectstart', (e) => {
            if (this.activeTouches.size > 0) {
                e.preventDefault();
            }
        }, { passive: false });
        
        // Prevent context menu on long press during educational interactions
        document.addEventListener('contextmenu', (e) => {
            const target = e.target;
            if (this.isEducationalElement(target)) {
                e.preventDefault();
            }
        }, { passive: false });
    }
    
    handleTouchStart(event) {
        event.preventDefault(); // Prevent default iOS behaviors
        
        const touch = event.changedTouches[0];
        const touchId = touch.identifier;
        this.touchStartTime = Date.now();
        
        // Store touch information
        this.activeTouches.set(touchId, {
            startX: touch.clientX,
            startY: touch.clientY,
            currentX: touch.clientX,
            currentY: touch.clientY,
            target: touch.target,
            isDragging: false
        });
        
        // Create and dispatch synthetic mousedown event
        const mouseEvent = this.createMouseEvent('mousedown', touch, event);
        touch.target.dispatchEvent(mouseEvent);
        
        // Special handling for draggable elements
        if (this.isDraggableElement(touch.target)) {
            this.setupDragOperation(touch, touchId);
        }
    }
    
    handleTouchMove(event) {
        event.preventDefault();
        
        const touch = event.changedTouches[0];
        const touchId = touch.identifier;
        const touchData = this.activeTouches.get(touchId);
        
        if (!touchData) return;
        
        // Update position
        touchData.currentX = touch.clientX;
        touchData.currentY = touch.clientY;
        
        // Calculate distance moved
        const deltaX = touch.clientX - touchData.startX;
        const deltaY = touch.clientY - touchData.startY;
        const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);
        
        // Determine if this is a drag operation
        if (!touchData.isDragging && distance > this.dragThreshold) {
            touchData.isDragging = true;
            
            // Dispatch dragstart for draggable elements
            if (this.isDraggableElement(touchData.target)) {
                const dragStartEvent = this.createDragEvent('dragstart', touch, event);
                touchData.target.dispatchEvent(dragStartEvent);
            }
        }
        
        // Create appropriate mouse event
        const eventType = touchData.isDragging ? 'mousemove' : 'mousemove';
        const mouseEvent = this.createMouseEvent(eventType, touch, event);
        touchData.target.dispatchEvent(mouseEvent);
        
        // Handle drag operations
        if (touchData.isDragging) {
            this.handleDragMove(touch, touchData, event);
        }
    }
    
    handleTouchEnd(event) {
        event.preventDefault();
        
        const touch = event.changedTouches[0];
        const touchId = touch.identifier;
        const touchData = this.activeTouches.get(touchId);
        
        if (!touchData) return;
        
        const touchDuration = Date.now() - this.touchStartTime;
        const isQuickTap = touchDuration < 200 && !touchData.isDragging;
        
        // Handle different end scenarios
        if (touchData.isDragging) {
            // End drag operation
            this.handleDragEnd(touch, touchData, event);
        } else if (isQuickTap) {
            // Handle as click
            const clickEvent = this.createMouseEvent('click', touch, event);
            touch.target.dispatchEvent(clickEvent);
        }
        
        // Always dispatch mouseup
        const mouseUpEvent = this.createMouseEvent('mouseup', touch, event);
        touchData.target.dispatchEvent(mouseUpEvent);
        
        // Clean up
        this.activeTouches.delete(touchId);
    }
    
    createMouseEvent(type, touch, originalEvent) {
        return new MouseEvent(type, {
            bubbles: true,
            cancelable: true,
            view: window,
            clientX: touch.clientX,
            clientY: touch.clientY,
            screenX: touch.screenX,
            screenY: touch.screenY,
            button: 0, // Left mouse button
            buttons: type === 'mouseup' ? 0 : 1,
            relatedTarget: null
        });
    }
    
    createDragEvent(type, touch, originalEvent) {
        // Create a synthetic drag event for HTML5 drag and drop
        const dragEvent = new DragEvent(type, {
            bubbles: true,
            cancelable: true,
            view: window,
            clientX: touch.clientX,
            clientY: touch.clientY,
            dataTransfer: new DataTransfer()
        });
        
        return dragEvent;
    }
    
    isDraggableElement(element) {
        // Check if element or its parents are draggable
        let current = element;
        while (current && current !== document.body) {
            if (current.draggable === true || 
                current.classList.contains('draggable') ||
                current.classList.contains('drag-item') ||
                current.getAttribute('data-draggable') === 'true') {
                return true;
            }
            current = current.parentElement;
        }
        return false;
    }
    
    isEducationalElement(element) {
        // Identify iReady educational interactive elements
        const educationalClasses = [
            'math-problem', 'drag-item', 'answer-choice', 
            'interactive-element', 'lesson-content', 'activity-item'
        ];
        
        return educationalClasses.some(className => 
            element.classList.contains(className) ||
            element.closest(`.${className}`)
        );
    }
    
    setupDragOperation(touch, touchId) {
        // Configure element for smooth dragging
        const element = touch.target;
        element.style.touchAction = 'none';
        element.style.userSelect = 'none';
        element.style.webkitUserSelect = 'none';
        
        // Add visual feedback
        element.style.opacity = '0.8';
        element.style.transform = 'scale(1.05)';
        element.style.zIndex = '1000';
        element.style.position = 'relative';
    }
    
    handleDragMove(touch, touchData, event) {
        const element = touchData.target;
        
        // Update element position for visual feedback
        const deltaX = touch.clientX - touchData.startX;
        const deltaY = touch.clientY - touchData.startY;
        
        element.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(1.05)`;
        
        // Find drop target under touch point
        element.style.pointerEvents = 'none'; // Temporarily disable to find element underneath
        const elementBelow = document.elementFromPoint(touch.clientX, touch.clientY);
        element.style.pointerEvents = 'auto';
        
        // Dispatch dragover event on potential drop target
        if (elementBelow && this.isDropTarget(elementBelow)) {
            const dragOverEvent = this.createDragEvent('dragover', touch, event);
            elementBelow.dispatchEvent(dragOverEvent);
        }
    }
    
    handleDragEnd(touch, touchData, event) {
        const element = touchData.target;
        
        // Reset visual state
        element.style.opacity = '';
        element.style.transform = '';
        element.style.zIndex = '';
        element.style.touchAction = '';
        
        // Find final drop target
        element.style.pointerEvents = 'none';
        const dropTarget = document.elementFromPoint(touch.clientX, touch.clientY);
        element.style.pointerEvents = 'auto';
        
        // Handle drop
        if (dropTarget && this.isDropTarget(dropTarget)) {
            const dropEvent = this.createDragEvent('drop', touch, event);
            dropTarget.dispatchEvent(dropEvent);
            
            // Dispatch dragend on original element
            const dragEndEvent = this.createDragEvent('dragend', touch, event);
            element.dispatchEvent(dragEndEvent);
        }
    }
    
    isDropTarget(element) {
        // Check if element can accept drops
        return element.classList.contains('drop-zone') ||
               element.classList.contains('answer-area') ||
               element.getAttribute('data-drop-target') === 'true';
    }
    
    handleTouchCancel(event) {
        // Clean up all active touches
        for (const [touchId, touchData] of this.activeTouches) {
            if (touchData.target) {
                touchData.target.style.opacity = '';
                touchData.target.style.transform = '';
                touchData.target.style.zIndex = '';
            }
        }
        this.activeTouches.clear();
    }
}

// Initialize touch polyfill immediately
const touchPolyfill = new TouchEventPolyfill();

// Re-initialize on dynamic content changes
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            // New content loaded, ensure touch events are properly handled
            console.log('New interactive content detected, touch polyfill active');
        }
    });
});

observer.observe(document.body, { childList: true, subtree: true });
```

<div style="background: #f8f9fa; border-left: 5px solid #17a2b8; padding: 20px; margin: 20px 0; border-radius: 0 8px 8px 0;">
    <h5 style="color: #0c5460; margin-top: 0;">Touch Event Conversion Results</h5>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-top: 15px;">
        <div>
            <strong style="color: #dc3545;">❌ Before Polyfill:</strong><br>
            <small>• Draggable elements unresponsive<br>• Touch events ignored<br>• No drag-and-drop functionality<br>• Math problems unsolvable</small>
        </div>
        <div>
            <strong style="color: #28a745;">✅ After Polyfill:</strong><br>
            <small>• Touch → Mouse event conversion<br>• Drag operations work smoothly<br>• Educational interactions functional<br>• iOS gestures properly prevented</small>
        </div>
    </div>
</div>

## Chapter 5: The Missing Button Crisis {#missing-buttons}

A critical usability issue emerged when we discovered that essential "DONE" buttons were consistently hidden below the viewport fold. Students could complete lessons but couldn't submit their work because the completion buttons were inaccessible.

Our solution combined MutationObserver DOM monitoring with automatic button detection. When new content loaded, our scripts would scan for completion buttons and programmatically scroll them into view. As a failsafe, we implemented custom button injection for cases where the original buttons remained unreachable.

```javascript
// Intelligent button detection and accessibility system
class ButtonAccessibilityManager {
    constructor() {
        this.buttonSelectors = [
            'button[data-action="done"]',
            '.done-button', '.submit-button', '.next-button',
            'button:contains("DONE")', 'button:contains("Submit")',
            'input[type="submit"]', '[role="button"][aria-label*="done"]'
        ];
        this.fallbackButtonInjected = false;
        this.setupMutationObserver();
        this.startPeriodicChecks();
    }
    
    setupMutationObserver() {
        // Watch for dynamically added content
        const observer = new MutationObserver((mutations) => {
            let shouldCheckButtons = false;
            
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            // Check if new content contains buttons or forms
                            if (node.tagName === 'BUTTON' || 
                                node.querySelector('button') ||
                                node.classList.contains('lesson-content') ||
                                node.classList.contains('activity-container')) {
                                shouldCheckButtons = true;
                            }
                        }
                    });
                }
            });
            
            if (shouldCheckButtons) {
                // Delay to allow content to fully render
                setTimeout(() => this.checkAndFixButtons(), 500);
            }
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['style', 'class']
        });
        
        console.log('Button accessibility observer initialized');
    }
    
    startPeriodicChecks() {
        // Check every 3 seconds for missing buttons
        setInterval(() => {
            this.checkAndFixButtons();
        }, 3000);
        
        // Also check on scroll events (user might be looking for button)
        document.addEventListener('scroll', this.debounce(() => {
            this.checkAndFixButtons();
        }, 1000));
    }
    
    checkAndFixButtons() {
        const buttons = this.findAllButtons();
        const hiddenButtons = buttons.filter(btn => this.isButtonHidden(btn));
        
        if (hiddenButtons.length > 0) {
            console.log(`Found ${hiddenButtons.length} hidden buttons, making accessible`);
            
            hiddenButtons.forEach(button => {
                this.makeButtonAccessible(button);
            });
        } else if (buttons.length === 0 && this.shouldHaveDoneButton()) {
            // No buttons found but context suggests there should be one
            this.injectFallbackButton();
        }
    }
    
    findAllButtons() {
        const buttons = [];
        
        this.buttonSelectors.forEach(selector => {
            try {
                if (selector.includes(':contains')) {
                    // Handle :contains pseudo-selector manually
                    const text = selector.match(/:contains\("([^"]+)"\)/)[1];
                    const elements = document.querySelectorAll('button');
                    elements.forEach(el => {
                        if (el.textContent.toLowerCase().includes(text.toLowerCase())) {
                            buttons.push(el);
                        }
                    });
                } else {
                    const elements = document.querySelectorAll(selector);
                    buttons.push(...elements);
                }
            } catch (e) {
                // Skip invalid selectors
            }
        });
        
        // Remove duplicates
        return [...new Set(buttons)];
    }
    
    isButtonHidden(button) {
        const rect = button.getBoundingClientRect();
        const style = window.getComputedStyle(button);
        
        // Check various ways a button can be hidden
        return (
            // Outside viewport
            rect.bottom > window.innerHeight ||
            rect.top < 0 ||
            rect.right > window.innerWidth ||
            rect.left < 0 ||
            
            // CSS hidden
            style.display === 'none' ||
            style.visibility === 'hidden' ||
            style.opacity === '0' ||
            
            // Dimensionally hidden
            rect.width === 0 ||
            rect.height === 0 ||
            
            // Behind other elements
            this.isButtonObscured(button)
        );
    }
    
    isButtonObscured(button) {
        const rect = button.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        const elementAtPoint = document.elementFromPoint(centerX, centerY);
        return elementAtPoint !== button && !button.contains(elementAtPoint);
    }
    
    makeButtonAccessible(button) {
        // Multiple strategies to make button accessible
        
        // Strategy 1: Scroll into view
        try {
            button.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center',
                inline: 'center'
            });
            
            // Wait and verify if it's now visible
            setTimeout(() => {
                if (this.isButtonHidden(button)) {
                    this.applyEmergencyButtonFix(button);
                }
            }, 1000);
            
        } catch (e) {
            // Fallback if scrollIntoView fails
            this.applyEmergencyButtonFix(button);
        }
    }
    
    applyEmergencyButtonFix(button) {
        // Force button to be visible and accessible
        const originalStyle = button.getAttribute('style') || '';
        
        button.style.cssText = `
            ${originalStyle}
            position: fixed !important;
            bottom: 20px !important;
            right: 20px !important;
            z-index: 10000 !important;
            background: #007bff !important;
            color: white !important;
            padding: 12px 24px !important;
            border: none !important;
            border-radius: 8px !important;
            font-size: 16px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            cursor: pointer !important;
        `;
        
        // Add pulsing animation to draw attention
        button.style.animation = 'pulse 2s infinite';
        
        // Inject pulse animation if not exists
        if (!document.querySelector('#pulse-animation')) {
            const style = document.createElement('style');
            style.id = 'pulse-animation';
            style.textContent = `
                @keyframes pulse {
                    0% { transform: scale(1); }
                    50% { transform: scale(1.05); }
                    100% { transform: scale(1); }
                }
            `;
            document.head.appendChild(style);
        }
        
        console.log('Applied emergency button fix:', button.textContent);
    }
    
    shouldHaveDoneButton() {
        // Heuristics to determine if current context should have a done button
        const indicators = [
            document.querySelector('.lesson-content'),
            document.querySelector('.activity-container'),
            document.querySelector('.math-problem'),
            document.querySelector('.question-container'),
            document.querySelector('form')
        ];
        
        return indicators.some(el => el !== null);
    }
    
    injectFallbackButton() {
        if (this.fallbackButtonInjected) return;
        
        const fallbackButton = document.createElement('button');
        fallbackButton.textContent = 'DONE';
        fallbackButton.className = 'fallback-done-button';
        fallbackButton.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 10001;
            background: #28a745;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            cursor: pointer;
            animation: slideInUp 0.5s ease-out;
        `;
        
        // Add click handler that tries to find and trigger the real done action
        fallbackButton.addEventListener('click', (e) => {
            e.preventDefault();
            this.triggerDoneAction();
        });
        
        document.body.appendChild(fallbackButton);
        this.fallbackButtonInjected = true;
        
        console.log('Injected fallback DONE button');
    }
    
    triggerDoneAction() {
        // Try multiple strategies to trigger the done action
        const strategies = [
            () => this.findAndClickHiddenButton(),
            () => this.triggerFormSubmit(),
            () => this.simulateKeyboardShortcut(),
            () => this.triggerCustomEvent()
        ];
        
        for (const strategy of strategies) {
            try {
                if (strategy()) {
                    console.log('Successfully triggered done action');
                    return;
                }
            } catch (e) {
                console.log('Strategy failed:', e.message);
            }
        }
        
        console.warn('All done action strategies failed');
    }
    
    findAndClickHiddenButton() {
        const allButtons = document.querySelectorAll('button, input[type="submit"]');
        for (const button of allButtons) {
            const text = button.textContent || button.value;
            if (/done|submit|next|continue/i.test(text)) {
                button.click();
                return true;
            }
        }
        return false;
    }
    
    triggerFormSubmit() {
        const forms = document.querySelectorAll('form');
        if (forms.length > 0) {
            forms[0].submit();
            return true;
        }
        return false;
    }
    
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Initialize button accessibility manager
const buttonManager = new ButtonAccessibilityManager();

// Add CSS animations
const animationStyles = document.createElement('style');
animationStyles.textContent = `
    @keyframes slideInUp {
        from {
            transform: translateY(100px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(animationStyles);
```

<div style="background: linear-gradient(45deg, #ff6b6b, #ee5a24); color: white; border-radius: 12px; padding: 25px; margin: 25px 0;">
    <h4 style="text-align: center; margin-bottom: 20px; color: white;">The Missing Button Problem</h4>
    
    <div style="display: flex; justify-content: space-between; align-items: stretch; gap: 20px;">
        <!-- Problem Visualization -->
        <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px;">
            <h5 style="color: white; margin-top: 0;">🔍 The Problem:</h5>
            <div style="background: #2c3e50; border-radius: 8px; padding: 15px; position: relative; height: 120px; overflow: hidden;">
                <div style="background: #3498db; height: 80px; border-radius: 4px; margin-bottom: 10px; display: flex; align-items: center; justify-content: center; font-size: 12px;">
                    Math Lesson Content
                </div>
                <div style="position: absolute; bottom: -15px; left: 10px; right: 10px; background: #e74c3c; color: white; padding: 8px; border-radius: 4px; text-align: center; font-size: 10px;">
                    DONE Button (Hidden Below)
                </div>
            </div>
            <small style="display: block; margin-top: 10px; opacity: 0.8;">Students can't submit completed work</small>
        </div>
        
        <!-- Solution -->
        <div style="flex: 1; background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px;">
            <h5 style="color: white; margin-top: 0;">✅ The Solution:</h5>
            <div style="background: #27ae60; border-radius: 8px; padding: 15px; position: relative; height: 120px;">
                <div style="background: #3498db; height: 60px; border-radius: 4px; margin-bottom: 10px; display: flex; align-items: center; justify-content: center; font-size: 12px;">
                    Math Lesson Content
                </div>
                <div style="position: absolute; bottom: 10px; right: 10px; background: #2ecc71; color: white; padding: 8px 16px; border-radius: 4px; font-size: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); animation: pulse 2s infinite;">
                    DONE
                </div>
            </div>
            <small style="display: block; margin-top: 10px; opacity: 0.8;">Auto-detected and repositioned</small>
        </div>
    </div>
    
    <div style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px; font-size: 14px;">
        <strong>Detection Methods:</strong> MutationObserver + Periodic scanning + Element visibility analysis + Fallback injection
    </div>
</div>

## Chapter 6: iOS WebView Configuration Deep Dive {#webview-configuration}

iOS WebView's default behaviors conflicted with iReady's expectations at every level. ScrollView bounce effects interfered with lesson scrolling, content insets affected layout calculations, and gesture recognizers captured touches meant for educational interactions.

We systematically disabled iOS-specific features: bounce scrolling, zoom gestures, link previews, and content inset adjustments. Each configuration change required careful testing to ensure we didn't break legitimate iOS functionality while enabling desktop-style interactions.

## Chapter 7: Network Request Interception and Modification {#network-requests}

iReady's AJAX requests expected desktop browser headers and cookie configurations that didn't exist in iOS WebView. API calls were failing silently, preventing lesson progress from saving and content from loading properly.

We implemented comprehensive request interception using XMLHttpRequest and Fetch API proxying. Our system automatically injected required headers, managed cross-domain cookies, and provided detailed logging for debugging network-related issues.

```javascript
// Comprehensive network request interception and modification system
class NetworkInterceptor {
    constructor() {
        this.requestLog = [];
        this.maxLogEntries = 100;
        this.domainConfigs = new Map();
        this.setupDomainConfigurations();
        this.interceptFetch();
        this.interceptXMLHttpRequest();
        this.setupErrorHandling();
    }
    
    setupDomainConfigurations() {
        // Configure headers and behaviors for different domains
        this.domainConfigs.set('iready.com', {
            requiredHeaders: {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin'
            },
            credentials: 'include',
            mode: 'cors',
            requiresCSRF: true
        });
        
        this.domainConfigs.set('clever.com', {
            requiredHeaders: {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json',
                'Origin': 'https://clever.com',
                'Referer': 'https://clever.com/'
            },
            credentials: 'include',
            mode: 'cors',
            requiresAuth: true
        });
        
        this.domainConfigs.set('cdnjs.cloudflare.com', {
            requiredHeaders: {
                'Accept': '*/*',
                'Cache-Control': 'max-age=3600'
            },
            credentials: 'omit',
            mode: 'cors'
        });
    }
    
    interceptFetch() {
        const originalFetch = window.fetch;
        
        window.fetch = async (resource, options = {}) => {
            const url = typeof resource === 'string' ? resource : resource.url;
            const method = options.method || 'GET';
            
            // Log request
            const requestId = this.generateRequestId();
            this.logRequest(requestId, method, url, options);
            
            try {
                // Modify request based on domain configuration
                const modifiedOptions = this.modifyRequestOptions(url, options);
                
                // Execute request
                const startTime = Date.now();
                const response = await originalFetch(resource, modifiedOptions);
                const duration = Date.now() - startTime;
                
                // Log response
                this.logResponse(requestId, response.status, duration, response.headers);
                
                // Handle special response cases
                if (this.requiresSpecialHandling(url, response)) {
                    return this.handleSpecialResponse(url, response);
                }
                
                return response;
                
            } catch (error) {
                this.logError(requestId, error);
                
                // Attempt recovery for known issues
                if (this.canRetryRequest(url, error)) {
                    console.log(`Retrying failed request: ${url}`);
                    return this.retryRequest(resource, options);
                }
                
                throw error;
            }
        };
        
        console.log('Fetch API intercepted successfully');
    }
    
    interceptXMLHttpRequest() {
        const originalXHR = window.XMLHttpRequest;
        const self = this;
        
        window.XMLHttpRequest = function() {
            const xhr = new originalXHR();
            const originalOpen = xhr.open;
            const originalSend = xhr.send;
            const originalSetRequestHeader = xhr.setRequestHeader;
            
            let method, url, headers = {};
            
            // Intercept open method
            xhr.open = function(m, u, async, user, password) {
                method = m;
                url = u;
                return originalOpen.call(this, m, u, async, user, password);
            };
            
            // Intercept setRequestHeader
            xhr.setRequestHeader = function(name, value) {
                headers[name] = value;
                return originalSetRequestHeader.call(this, name, value);
            };
            
            // Intercept send method
            xhr.send = function(data) {
                const requestId = self.generateRequestId();
                self.logRequest(requestId, method, url, { headers, body: data });
                
                // Inject required headers
                const config = self.getDomainConfig(url);
                if (config) {
                    Object.entries(config.requiredHeaders).forEach(([name, value]) => {
                        if (!headers[name]) {
                            xhr.setRequestHeader(name, value);
                        }
                    });
                    
                    // Add CSRF token if required
                    if (config.requiresCSRF) {
                        const csrfToken = self.getCSRFToken();
                        if (csrfToken) {
                            xhr.setRequestHeader('X-CSRF-Token', csrfToken);
                        }
                    }
                    
                    // Add authorization if required
                    if (config.requiresAuth) {
                        const authToken = self.getAuthToken(url);
                        if (authToken) {
                            xhr.setRequestHeader('Authorization', authToken);
                        }
                    }
                }
                
                // Log response when ready
                const originalOnReadyStateChange = xhr.onreadystatechange;
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4) {
                        self.logResponse(requestId, xhr.status, 0, {
                            'content-type': xhr.getResponseHeader('content-type')
                        });
                    }
                    if (originalOnReadyStateChange) {
                        originalOnReadyStateChange.call(this);
                    }
                };
                
                return originalSend.call(this, data);
            };
            
            return xhr;
        };
        
        console.log('XMLHttpRequest intercepted successfully');
    }
    
    modifyRequestOptions(url, options) {
        const config = this.getDomainConfig(url);
        if (!config) return options;
        
        const modifiedOptions = { ...options };
        
        // Merge headers
        const headers = new Headers(options.headers || {});
        Object.entries(config.requiredHeaders).forEach(([name, value]) => {
            if (!headers.has(name)) {
                headers.set(name, value);
            }
        });
        
        // Set credentials and mode
        modifiedOptions.headers = headers;
        modifiedOptions.credentials = config.credentials;
        modifiedOptions.mode = config.mode;
        
        // Add special tokens
        if (config.requiresCSRF) {
            const csrfToken = this.getCSRFToken();
            if (csrfToken) {
                headers.set('X-CSRF-Token', csrfToken);
            }
        }
        
        if (config.requiresAuth) {
            const authToken = this.getAuthToken(url);
            if (authToken) {
                headers.set('Authorization', authToken);
            }
        }
        
        return modifiedOptions;
    }
    
    getDomainConfig(url) {
        try {
            const domain = new URL(url).hostname;
            for (const [configDomain, config] of this.domainConfigs) {
                if (domain.includes(configDomain)) {
                    return config;
                }
            }
        } catch (e) {
            // Invalid URL
        }
        return null;
    }
    
    getCSRFToken() {
        // Try multiple methods to get CSRF token
        const methods = [
            () => document.querySelector('meta[name="csrf-token"]')?.content,
            () => document.querySelector('input[name="_token"]')?.value,
            () => this.getCookieValue('csrf_token'),
            () => this.getCookieValue('XSRF-TOKEN')
        ];
        
        for (const method of methods) {
            try {
                const token = method();
                if (token) return token;
            } catch (e) {
                // Continue to next method
            }
        }
        
        return null;
    }
    
    getAuthToken(url) {
        const domain = new URL(url).hostname;
        
        if (domain.includes('clever.com')) {
            return this.getCookieValue('clever_session');
        }
        
        if (domain.includes('iready.com')) {
            return this.getCookieValue('iready_session');
        }
        
        return null;
    }
    
    getCookieValue(name) {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
            const [cookieName, cookieValue] = cookie.trim().split('=');
            if (cookieName === name) {
                return decodeURIComponent(cookieValue);
            }
        }
        return null;
    }
    
    requiresSpecialHandling(url, response) {
        // Check if response needs special processing
        return (
            response.status === 401 || // Unauthorized
            response.status === 403 || // Forbidden  
            response.status === 419 || // CSRF token expired
            (response.status === 302 && url.includes('login')) // Redirect to login
        );
    }
    
    async handleSpecialResponse(url, response) {
        if (response.status === 401 || response.status === 403) {
            console.log('Authentication failed, attempting token refresh');
            await this.refreshAuthTokens();
            // Return original response - retry will happen at higher level
            return response;
        }
        
        if (response.status === 419) {
            console.log('CSRF token expired, refreshing');
            await this.refreshCSRFToken();
            return response;
        }
        
        return response;
    }
    
    async refreshAuthTokens() {
        // Attempt to refresh authentication tokens
        try {
            // This would trigger re-authentication flow
            console.log('Triggering authentication refresh...');
            // Implementation would depend on specific auth system
        } catch (e) {
            console.error('Failed to refresh auth tokens:', e);
        }
    }
    
    async refreshCSRFToken() {
        // Get fresh CSRF token
        try {
            const response = await fetch('/csrf-token', { credentials: 'include' });
            if (response.ok) {
                const data = await response.json();
                if (data.token) {
                    // Update meta tag or hidden input
                    const metaTag = document.querySelector('meta[name="csrf-token"]');
                    if (metaTag) {
                        metaTag.content = data.token;
                    }
                }
            }
        } catch (e) {
            console.error('Failed to refresh CSRF token:', e);
        }
    }
    
    canRetryRequest(url, error) {
        // Determine if request should be retried
        return (
            error.name === 'NetworkError' ||
            error.message.includes('Failed to fetch') ||
            error.message.includes('Network request failed')
        );
    }
    
    async retryRequest(resource, options) {
        // Wait briefly before retry
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Retry with original fetch (will go through our interceptor again)
        return window.fetch(resource, options);
    }
    
    generateRequestId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
    
    logRequest(id, method, url, options) {
        const logEntry = {
            id,
            type: 'request',
            timestamp: new Date().toISOString(),
            method,
            url,
            headers: options.headers,
            body: options.body
        };
        
        this.addToLog(logEntry);
        console.log(`[REQ ${id}] ${method} ${url}`);
    }
    
    logResponse(id, status, duration, headers) {
        const logEntry = {
            id,
            type: 'response',
            timestamp: new Date().toISOString(),
            status,
            duration,
            headers
        };
        
        this.addToLog(logEntry);
        console.log(`[RES ${id}] ${status} (${duration}ms)`);
    }
    
    logError(id, error) {
        const logEntry = {
            id,
            type: 'error',
            timestamp: new Date().toISOString(),
            error: error.message,
            stack: error.stack
        };
        
        this.addToLog(logEntry);
        console.error(`[ERR ${id}] ${error.message}`);
    }
    
    addToLog(entry) {
        this.requestLog.push(entry);
        if (this.requestLog.length > this.maxLogEntries) {
            this.requestLog.shift();
        }
    }
    
    setupErrorHandling() {
        // Global error handler for unhandled network errors
        window.addEventListener('unhandledrejection', (event) => {
            if (event.reason && event.reason.message && 
                event.reason.message.includes('fetch')) {
                console.log('Caught unhandled fetch rejection:', event.reason);
                // Could implement additional recovery logic here
            }
        });
    }
    
    // Debug method to inspect request logs
    getRequestLogs() {
        return this.requestLog;
    }
    
    // Debug method to get recent failed requests
    getFailedRequests() {
        return this.requestLog.filter(entry => 
            entry.type === 'error' || 
            (entry.type === 'response' && entry.status >= 400)
        );
    }
}

// Initialize network interceptor immediately
const networkInterceptor = new NetworkInterceptor();

// Expose debug interface to global scope for debugging
window.debugNetwork = {
    getLogs: () => networkInterceptor.getRequestLogs(),
    getFailures: () => networkInterceptor.getFailedRequests(),
    clearLogs: () => networkInterceptor.requestLog = []
};
```

<div style="background: #e8f4fd; border: 2px solid #bee5eb; border-radius: 12px; padding: 25px; margin: 25px 0;">
    <h4 style="color: #0c5460; text-align: center; margin-bottom: 20px;">Network Request Flow Transformation</h4>
    
    <div style="display: flex; flex-direction: column; gap: 15px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="background: #dc3545; color: white; padding: 8px 12px; border-radius: 6px; min-width: 80px; text-align: center; font-weight: bold;">
                BEFORE
            </div>
            <div style="flex: 1; padding: 12px; background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 6px;">
                <strong>iOS WebView Request:</strong><br>
                <code style="font-size: 12px; color: #721c24;">
                fetch('/api/progress') → ❌ 403 Forbidden (Missing headers)
                </code>
            </div>
        </div>
        
        <div style="text-align: center; color: #6c757d; font-size: 24px;">↓ INTERCEPT & MODIFY ↓</div>
        
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="background: #28a745; color: white; padding: 8px 12px; border-radius: 6px; min-width: 80px; text-align: center; font-weight: bold;">
                AFTER
            </div>
            <div style="flex: 1; padding: 12px; background: #d4edda; border: 1px solid #c3e6cb; border-radius: 6px;">
                <strong>Modified Request:</strong><br>
                <code style="font-size: 12px; color: #155724;">
                fetch('/api/progress', {<br>
                &nbsp;&nbsp;headers: { 'X-Requested-With': 'XMLHttpRequest', 'X-CSRF-Token': '...' }<br>
                }) → ✅ 200 OK
                </code>
            </div>
        </div>
    </div>
    
    <div style="margin-top: 20px; padding: 15px; background: #cfe2ff; border-left: 4px solid #0d6efd; border-radius: 0 8px 8px 0;">
        <strong style="color: #084298;">Headers Auto-Injected:</strong><br>
        <small style="color: #084298;">X-Requested-With • Accept • CSRF-Token • Authorization • Origin • Referer • Cache-Control</small>
    </div>
</div>

## Chapter 8: Advanced Browser Fingerprinting Evasion {#fingerprinting-evasion}

As our spoofing became more sophisticated, we discovered that iReady employed increasingly subtle detection methods. The platform checked window dimensions, device pixel ratios, media query results, and even the existence of specific JavaScript APIs.

Our final solution involved complete environment spoofing: replacing the screen object, overriding window dimensions, manipulating CSS media queries, and removing touch-related APIs entirely. The goal was to create a perfect illusion of a desktop Firefox browser running on macOS.

## Chapter 9: Dynamic Content and Layout Adaptation {#dynamic-content}

iReady's lessons loaded content dynamically, often breaking our static fixes as new DOM elements appeared. Math problems, reading passages, and interactive widgets each presented unique mobile compatibility challenges.

We developed a reactive system using MutationObserver to detect content changes and automatically apply fixes to new elements. This included re-running spoofing scripts, adjusting zoom levels, and ensuring interactive elements remained accessible on the smaller mobile viewport.

## Chapter 10: Performance Optimization and Memory Management {#performance-optimization}

Our extensive JavaScript injection and polyfills created performance bottlenecks, especially on older iOS devices. Console logging, event listeners, and DOM monitoring were consuming excessive memory and CPU cycles.

Optimization involved selective script injection based on detected content types, throttled console output, and efficient event handler management. We implemented a minimal spoofing approach that achieved compatibility while preserving device performance.

## Chapter 11: Touch Gesture Conflicts and Resolution {#gesture-conflicts}

iOS's built-in gestures - pinch-to-zoom, swipe navigation, long-press menus - constantly interfered with iReady's educational interactions. Students couldn't complete math problems because iOS was interpreting their touches as system gestures.

Our solution required surgical gesture prevention: blocking specific iOS behaviors while preserving essential accessibility features. We implemented custom gesture recognizers that could differentiate between educational interactions and legitimate system gestures.

## Chapter 12: Cross-Lesson Compatibility Testing {#compatibility-testing}

Each iReady lesson type - math, reading, vocabulary - presented unique technical challenges. What worked for drag-and-drop math problems broke reading comprehension interfaces, and vocabulary lessons had entirely different interaction patterns.

We developed comprehensive testing protocols to validate fixes across lesson types, grade levels, and subject areas. This revealed edge cases where our spoofing was insufficient and required lesson-specific workarounds.

## Chapter 13: Error Handling and Debugging Infrastructure {#error-handling}

Debugging WebView issues on iOS required custom logging infrastructure since traditional browser developer tools weren't available. JavaScript errors, network failures, and touch event problems needed to be captured and analyzed remotely.

We built a comprehensive error reporting system that bridged console messages to the native iOS app, provided network request logging, and captured JavaScript execution traces. This infrastructure was essential for diagnosing issues that only occurred on physical devices.

## Chapter 14: Security Considerations and Responsible Bypass {#security-considerations}

Throughout this process, we maintained focus on educational access rather than malicious platform circumvention. Our spoofing techniques were designed to enable learning, not to violate terms of service or compromise system security.

We implemented minimal necessary spoofing, avoiding over-broad system modifications that could impact other applications or compromise user privacy. The goal was always educational equity, not platform exploitation.

## Chapter 15: Production Deployment and Stability {#production-deployment}

Moving from proof-of-concept to production-ready required extensive stability testing and fallback mechanisms. Our solution needed to work reliably across iOS versions, device types, and network conditions without requiring constant maintenance.

The final implementation included comprehensive error recovery, automatic retry mechanisms, and graceful degradation when spoofing failed. We achieved a stable solution that provided consistent access to iReady lessons on iOS devices.

## Conclusion: Technical Lessons and Educational Impact {#conclusion}

This project demonstrates the complex intersection of web standards, platform restrictions, and educational equity. While technically challenging, the effort successfully democratized access to educational content that was artificially restricted to specific hardware platforms.

The techniques developed here - browser fingerprinting evasion, touch event polyfills, dynamic content adaptation - represent a toolkit for breaking down platform silos in educational technology. Most importantly, students can now access their learning materials regardless of their family's hardware choices.
