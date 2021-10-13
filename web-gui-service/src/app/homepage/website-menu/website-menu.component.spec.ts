import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WebsiteMenuComponent } from './website-menu.component';

describe('WebsiteMenuComponent', () => {
  let component: WebsiteMenuComponent;
  let fixture: ComponentFixture<WebsiteMenuComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ WebsiteMenuComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(WebsiteMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
