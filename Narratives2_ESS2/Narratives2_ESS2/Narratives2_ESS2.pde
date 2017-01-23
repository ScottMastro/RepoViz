import krister.Ess.*;

AudioChannel myChannel;
FFT myFFT;
int sample_rate = 44100;  // sample rate of .wav file 
                          // KEEP CONSISTENT WITH VALUE FROM PYSYNTH!
int time_size = 2048;     // number of points in the FFT, 
                          // note: only half are used due to Nyquist frequencies

String wav_filename = "out.wav";
String words_filename = "commit_words.txt";
String dates_filename = "commit_dates.txt";

float threshold = 5;

int frame_rate = 30;
float commit_day_length = frame_rate * 1.2; // 1.2s to play a commit day, this value may need to be tweaked

boolean spiral = true;
int number_of_curves;  // number of top words being analyzed
int amplifier = 1000; // usually between 100 and 50000 (lower = higher resolving power but weaker visualization)
float min_cutoff = 0.01; // usually between 0 and 0.1 (minimium amplitude to visualize)
float frequency_array [] = {43.6535289291, 61.735412657, 123.470825314,
    246.941650628, 493.883301256, 987.766602512, 1975.53320502}; //note: length must = number_of_curves

curve  [] curve_array; // Array of the used frequencies

float text_x [];
float text_y [];
float intensity[];

int width = 1000;
int height = 700;

int x_center = width/2; // x position of the visualization
int y_center = height/2; // y position of the visualization

float rotation = PI*3/2; // rotation of the visualization

boolean playing = true; // Boolean to check if applet is playing or not

String[] commitWords = null; // list of commit words
String[] commitDates = null; // list of commit dates
int commitDatesPos = 0; // keeps track of the last commit date displayed

PImage prev_image = null;

int frame_count = 0;

void setup() {

  frameRate(frame_rate);
  size (width, height); 
  smooth();

  noFill();
  background(0);
  colorMode(HSB);

  Ess.start(this); // init Es
  myChannel=new AudioChannel(wav_filename); // load music file into a new AudioChannel
  myFFT=new FFT(time_size); // we want time_size/2 frequency bands, so we pass time_size
  myChannel.play(); // start the sound 

  noStroke();
  
   // Create the font
  textAlign(CENTER, CENTER);
  
  // read the commit dates text file in
  commitDates = loadStrings(dates_filename);
  // read the commit words text file in
  commitWords = loadStrings(words_filename);
  number_of_curves = commitWords.length;
  
  curve_array = new curve[number_of_curves]; // Array of the used frequencies
  text_x = new float[number_of_curves];
  text_y = new float[number_of_curves];
  intensity = new float[number_of_curves];

  // init the frequency Objects
  for (int i=0; i<number_of_curves; i++) { 
    curve_array[i] = new curve(i);
  }
  
} 

// ---------------------------------------------------------------------------------
// -------  code from http://code.compartmental.net/2007/03/21/fft-averages/ -------
// ---------------------------------------------------------------------------------

public float getBandWidth()
{
  return (2f/time_size) * (sample_rate/2f);
}
 
public int freqToIndex(float freq)
{
  // special case: freq is lower than the bandwidth of spectrum[0]
  if ( freq < getBandWidth()/2 ) return 0;
  // special case: freq is within the bandwidth of spectrum[1024]
  if ( freq > sample_rate/2 - getBandWidth()/2 ) return 1024;
  // all other cases
  float fraction = (float)freq/(float) sample_rate;
  int i = Math.round(time_size * fraction);
  return i;
}
// ---------------------------------------------------------------------------------


void draw() {

  if (playing) { // if music is playing
    if(prev_image != null)
      set(0, 0, prev_image);

  try{ myFFT.getSpectrum(myChannel); }// load spectrum
  catch (Exception e){ } //do nothing


  for (int i=0; i<number_of_curves; i++) {  // for the defined channel spectrum
  
      int index = freqToIndex(frequency_array[i]);
      float spectrum_val = myFFT.spectrum[index]; //amplitude value for given index (ie. frequency band)
      
      float val = 0;
      if(spectrum_val > min_cutoff)
        val = min(75, spectrum_val*amplifier);
        
      curve_array[i].draw_channel(val, i); //draw the curve
    }
  }
  
  int minSize = 6;
  for (int j=0; j<= text_x.length - 1; j++) {
    textFont(createFont("Georgia", min(32, max(minSize, intensity[j]))));
    fill(125*(sin(j*j) + 1), 255, 255, 100);
    text(commitWords[j], text_x[j] + 10, text_y[j] +10);
  }
  
  textFont(createFont("Georgia", 30));
  fill(0, 0, 255, 100);
  if (commitDatesPos >=  commitDates.length) {
    text(commitDates[commitDates.length -1], width - 160, height - 40);
    //print("Reached end of dates!");
  } else {
    text(commitDates[commitDatesPos], width - 160, height - 40);
  }
  
  if (frame_count == commit_day_length) {
    commitDatesPos ++;
    frame_count = 0;
  } else {
     frame_count ++;
  }
} 

// curve Class
// draw the curve for a frequency 
class curve {
  
  // the curve is a series of line segments; each segment is drawn from (x,y) to (x3,y3)
  // to slow the animation, each line segment is drawn in smaller portions from (x,y) to (x2,y2)
  float x;
  float y;
  float x2;
  float y2;
  float x3;
  float y3;
  float x_dist = 0;
  float y_dist = 0;
  float count = 0;

  // constructor
  curve(int i) {
    x = x_center;
    y = y_center;
    turn = (i+6); // controls how tightly each spiral turns
  }

  // gets the next position that falls on the curve
  void get_next_xy() {
    //if the whole line segment has been drawn, calculate the new line segment
    if(count == round(k/2)){
      count = 0;
      make_next_line();
    }
    //otherwise, continue drawing subsegments
    else
      finish_line();
  }

// ----------------------------------------------------------------------------------------------------------------
// -- code from  http://www.cs.cornell.edu/courses/cs100j/1998fa/lectures/lecture09/CUCSGraphicsApplication.java --
// ----------------------------------------------------------------------------------------------------------------

  float k= 1; // number of line segments drawn so far
  int turn;   // turn factor
  float d= .1;  // length of line segment k is k*d
   
  void make_next_line() {
    float theta= k*turn %360;
    float L= k*d;
    x3 = x+L*L*cos(theta*PI/180);
    y3 = y+L*L*sin(theta*PI/180);
          
    k= k+1;

// ---------------------------------------------------------------------------------
  
    x_dist = x3-x;
    y_dist = y3-y;
   
   finish_line();
    
  }
  
  //draw a subset of the current line segment
  void finish_line(){
    
    x2 = x + 1/(k/2) * x_dist;
    y2 = y + 1/(k/2) * y_dist;
    
    count++;
  }

  void draw_channel (float magnitude, int fan) {
    
    if(spiral)
      get_next_xy(); //calculating the next x and y positions
    else{
      int stroke_length = 1;
      y2 = stroke_length * sin((PI/(number_of_curves*2 - 1.5) * fan)+rotation);
      x2 = stroke_length * cos((PI/(number_of_curves*2 - 1.5) * fan)+rotation);

      //y2 = stroke_length * sin(radians((magnitude)*100)+(PI/spectrum_max * fan)+rotation);
      //x2 = stroke_length * cos(radians((magnitude)*100)+(PI/spectrum_max * fan)+rotation);
    }
    
    strokeWeight(magnitude);


    if (magnitude > threshold) {
      stroke(125*(sin(fan*fan) + 1), 255, 255, 10);
    }
    else {
      // if value lower then the thereshold draw white line
      strokeWeight(0.5); 
      stroke(255, 0, 255, 60);
    }

    if (spiral)
      line (x, y, x2, y2);
    else {
       line (x, y, x+x2, y+y2);
    }

    text_x[fan] = x;
    text_y[fan] = y;
    intensity[fan] = magnitude;

    if (spiral) {
      x = x2;
      y = y2;
    }
    else {
      x += x2;
      y += y2;
   }

    prev_image = get();
  }
}


void audioChannelDone(AudioChannel ch) {
  // event if channel stops
  playing = false;
  print("Finished");
}


public void stop() { 
  // event if applet stops
  Ess.stop(); 
  super.stop(); 

} 

