---
layout: default
title: Android Feedback
date: 2025-05-30
social_image: https://i.imgur.com/T7ovThQ.jpeg
---

<main id="main" tabindex="-1">
  <article>
    <h1 class="title">
      <span role="text">
        Android Feedback
      </span>
    </h1>
    <ul class="dot_list meta">
      <li>
        Posted <time datetime="2025-05-30">
          30 May 2025
        </time>
      </li>
    </ul>

    <div style="display: flex; gap: 15px; margin: 20px 0; flex-wrap: wrap;">
      <img src="https://i.imgur.com/qe6RVVK.png" style="flex: 1; width: 200px; height: auto; border-radius: 8px;" alt="blue"/>
      <img src="https://i.imgur.com/50Ntozk.png" style="flex: 1; width: 200px; height: auto; border-radius: 8px;" alt="blue"/>
    </div>

    <style>
      .qa-section {
        margin: 30px 0;
      }
      .question {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 5px solid #4f46e5;
        font-weight: 500;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      }
      .question::before {
        content: "Q: ";
        font-weight: bold;
        color: #fbbf24;
      }
      .answer {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        color: #1f2937;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        border-left: 5px solid #10b981;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      }
      .answer::before {
        content: "A: ";
        font-weight: bold;
        color: #059669;
      }
      .answer a {
        color: #2563eb;
        text-decoration: underline;
        font-weight: 500;
      }
      .answer a:hover {
        color: #1d4ed8;
      }
    </style>

    <div class="qa-section">
      <blockquote class="question">
        First.. on android the notification the status bar looks weird... with this blue color on it. Screen attached. By any chance there will be a dark theme?
      </blockquote>
      
      <blockquote class="answer">
        Oh yes, I use dark mode for the entire android device and like how it looks much better. Do you want just this app to be in dark mode but not the entire phone? We can add that.
      </blockquote>
    </div>

    <div class="qa-section">
      <blockquote class="question">
        When i select a series to watch or add to watchlist... the episodes and seasons are waaaaay down on the page...content rating, starring, genre etc above.. and its almost the last thing to find. I think it should be way above... kinda the first thing to check imo.
      </blockquote>
      
      <blockquote class="answer">
        Good point! Our designer liked it this way. I think if you get good at a quick scroll you can get down there very fast. But how about an option in settings? I'll make it so the user can decide if they are at the top or bottom.
      </blockquote>
    </div>

    <div class="qa-section">
      <blockquote class="question">
        On the progress part... could or should we see where we are at that the series? Like watched 10 ep from the 20 overall? even at a percentage or something. Maybe even a progress bar when we check out an episode there?! would be cool.
      </blockquote>
      
      <blockquote class="answer">
        Oh yes, definitely. The iOS version add this. Will add it.
      </blockquote>
    </div>

    <div class="qa-section">
      <blockquote class="question">
        The upcoming part ... why it show the past dates too? it show the 2 month ago came out episodes too... kinda weird imo. Upcoming means not out yet... not the past :)
      </blockquote>
      
      <blockquote class="answer">
        so this was a user request <a href="https://www.reddit.com/r/showffeur/comments/1kt0kb2/rewind_time_in_the_upcoming_tabs/">https://www.reddit.com/r/showffeur/comments/1kt0kb2/rewind_time_in_the_upcoming_tabs/</a> "The upcoming tabs in both tv shows and movies is forward looking. Allow me to scroll back in time to see when shows previously aired." I agree the term upcoming is confusing here. The scroll start in the middle so when you first open the view it should be scrolled down half way on "today". I think the reason im_johnlakeman requested this is because he wanted to see what he missed and didn't like it just leaving the way with no way to find it again. Lots of ways to solve this. Settings options, or a more clear "load history" button.
      </blockquote>
    </div>

    <div class="qa-section">
      <blockquote class="question">
        If on the progress part we check the 10th episode should it ask we wanna to check the previous episodes too to watched.. i mean with that one click and we can check out a whole season.
      </blockquote>
      
      <blockquote class="answer">
        On the progress part it always increments to the next available episode. So if the on S1E10 it'll goto S1E11 or S2E1 depending on how many episodes in the season. But if there are gaps like maybe S1E1 was marked watched but S1E2 was not you think all the gaps should get marked? I like it. Maybe an option for this in settings.
      </blockquote>
    </div>

    <div class="qa-section">
      <blockquote class="question">
        On progress part why it show episodes that not out yet? Should be show the ones are already out imo.
      </blockquote>
      
      <blockquote class="answer">
        That's fair. The issue is some hollywood people that work on the shows get early access. I'll add setting.
      </blockquote>
    </div>

    <div class="qa-section">
      <blockquote class="question">
        will be some stat page once or planning it?
      </blockquote>
      
      <blockquote class="answer">
        definitely! If you have some stats pages from other apps you like, please post screen shots.
      </blockquote>
    </div>

    <div class="qa-section">
      <blockquote class="question">
        maybe some another way to import data? like tvtime or any another site?
      </blockquote>
      
      <blockquote class="answer">
        in settings now there is import from trakt. But sure, we can add any other site out there that has a way to export their data.
      </blockquote>
    </div>
      
  </article>
</main>
