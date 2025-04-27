import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {BoardComponent} from './board/board.component';
import {CreateCardFormComponent} from './create-card-form/create-card-form.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, BoardComponent, CreateCardFormComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'App';
}
