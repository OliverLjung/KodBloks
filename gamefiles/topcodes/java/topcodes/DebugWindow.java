/*
 * @(#) DebugWindow.java
 * 
 * Tangible Object Placement Codes (TopCodes)
 * Copyright (c) 2007 Michael S. Horn
 * 
 *           Michael S. Horn (michael.horn@tufts.edu)
 *           Tufts University Computer Science
 *           161 College Ave.
 *           Medford, MA 02155
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License (version 2) as
 * published by the Free Software Foundation.
 * 
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 */
package topcodes;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.FilenameFilter;
import java.io.FileOutputStream;

import java.util.List;

import java.awt.*;
import java.awt.event.*;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.awt.geom.AffineTransform;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.UIManager;
import javax.swing.JFileChooser;

import java.lang.Math;
// import com.sun.image.codec.jpeg.*;



/**
 * Debug window for TopCode scanner
 *
 * @author Michael Horn
 * @version $Revision: 1.8 $, $Date: 2008/02/04 15:02:38 $
 */
public class DebugWindow
{
   /** The main app window */

   protected Scanner scanner;

   protected List spots;

   protected String file;


   public DebugWindow() {
      
      this.scanner = new Scanner();
      this.scanner.setMaxCodeDiameter(100);

      // create file list
      this.file = "bild.jpg";
      clear();

      loadTest();
   }



   public void clear() {
      this.spots      = null;
   }


//-----------------------------------------------------------------
// Load the next image from the test directory
//-----------------------------------------------------------------
   public void load(String file) {
      clear();
      if (file == null) return;
      if (!(new File(file)).exists()) return;

      
      try {
         long start_t = System.currentTimeMillis();
         this.spots = scanner.scan(file);
         start_t = System.currentTimeMillis() - start_t;
         System.out.println("Found " + spots.size() + " codes.");
         System.out.println(scanner.getCandidateCount() + " candidates.");
         System.out.println(scanner.getTestedCount() + " tested.");
         TopCode top;
         for (int i=0; i<spots.size(); i++) {
            top = (TopCode)spots.get(i);
            System.out.println("topcode="+ top.getCode() + ", pos=(" + Math.round(top.getCenterX()) + ","+ Math.round(top.getCenterY()) + ")");
         }
         System.out.println(start_t + "ms elapsed time.");
      }
      catch (IOException iox) {
         iox.printStackTrace();
      }
   }



   public void loadTest() {
      System.out.println(file);
      
      load(file);
   }


/**
 * main entry point
 */
   public static void main(String[] args) {
      
      //--------------------------------------------------
      // Schedule a job for the event-dispatching thread:
      // creating and showing this application's GUI.
      //--------------------------------------------------
      javax.swing.SwingUtilities.invokeLater(new Runnable() {
            public void run() {
               new DebugWindow();
            }
         });
   }
}

