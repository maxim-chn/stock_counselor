import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CollectStockDataComponent } from './collect-stock-data.component';

describe('CollectStockDataComponent', () => {
  let component: CollectStockDataComponent;
  let fixture: ComponentFixture<CollectStockDataComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CollectStockDataComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CollectStockDataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
