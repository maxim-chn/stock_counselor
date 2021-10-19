import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InvestmentFunctionalitiesMenuComponent } from './investment-functionalities-menu.component';

describe('InvestmentFunctionalitiesMenuComponent', () => {
  let component: InvestmentFunctionalitiesMenuComponent;
  let fixture: ComponentFixture<InvestmentFunctionalitiesMenuComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InvestmentFunctionalitiesMenuComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InvestmentFunctionalitiesMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
