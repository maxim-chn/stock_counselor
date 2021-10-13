import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CalculateInvestmentRecommendationComponent } from './calculate-investment-recommendation.component';

describe('CalculateInvestmentRecommendationComponent', () => {
  let component: CalculateInvestmentRecommendationComponent;
  let fixture: ComponentFixture<CalculateInvestmentRecommendationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CalculateInvestmentRecommendationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CalculateInvestmentRecommendationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
