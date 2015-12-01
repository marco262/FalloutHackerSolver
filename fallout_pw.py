from Tkinter import *
import wx

VERSION = "2.2"
LAST_UPDATED = "Nov 30, 2015"
wordlist = {} 

class MyFrame(wx.Frame):
    
    wordlist = {}

    def __init__(self, parent=None, id=-1, title=None):
        wx.Frame.__init__(self, parent, id, title)
        self.InitGui()

    def InitGui(self):
        fileMenu = wx.Menu()
        filemenu_clear = fileMenu.Append(-1, '&Clear List', 'Clears the passwords list and resets the app')
        self.Bind(wx.EVT_MENU, self.OnClear, filemenu_clear)
        fileMenu.AppendSeparator()
        filemenu_exit = fileMenu.Append(wx.ID_EXIT, 'E&xit', 'Exit Application')
        self.Bind(wx.EVT_MENU, self.OnExit, filemenu_exit)
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File')
        self.SetMenuBar(menuBar)

        self.p = wx.Panel(self)

        self.WordsBox = wx.ListBox(self.p, size=(150,300), choices=self.wordlist.keys())
        deleteWordButton = wx.Button(self.p, label="Delete Word")
        deleteWordButton.Bind(wx.EVT_BUTTON, self.OnDeleteWord)
        clearListButton = wx.Button(self.p, label="Clear List")
        clearListButton.Bind(wx.EVT_BUTTON, self.OnClear)
        
        self.AddWordBox = wx.TextCtrl(self.p, style=wx.TE_PROCESS_ENTER)
        self.AddWordBox.Bind(wx.EVT_TEXT_ENTER, self.OnAddWord)
        self.AddWordBox.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        addWordButton = wx.Button(self.p, label="Add", size=(50,-1))
        addWordButton.Bind(wx.EVT_BUTTON, self.OnAddWord)

        self.WordDropDown = wx.Choice(self.p)
        self.LettersDropDown = wx.Choice(self.p)
        goButton = wx.Button(self.p, label="Go", size=(30,-1))
        goButton.Bind(wx.EVT_BUTTON, self.OnGuessWord)
        self.SolutionText = "\n\nThe best word to try is:\n{0}\n"
        self.SolutionLabel = wx.StaticText(self.p, label=self.SolutionText.format(""))

        wordsStaticBox = wx.StaticBox(self.p, label='Possible Passwords')
        wordsSizer = wx.StaticBoxSizer(wordsStaticBox, wx.VERTICAL)
        wordsSizer.Add(self.WordsBox, 1, wx.EXPAND | wx.BOTTOM, border=5)
        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsSizer.Add(deleteWordButton, 1, wx.ALL, border=3)
        buttonsSizer.Add(clearListButton, 1, wx.ALL, border=3)
        wordsSizer.Add(buttonsSizer, 0)
        addSizer = wx.BoxSizer(wx.HORIZONTAL)
        addSizer.Add(self.AddWordBox, 1, wx.ALL, border=3)
        addSizer.Add(addWordButton, 0, wx.ALL, border=3)
        wordsSizer.Add(addSizer, 0)

        solutionStaticBox = wx.StaticBox(self.p, label='Solution')
        solutionSizer = wx.StaticBoxSizer(solutionStaticBox, wx.VERTICAL)
        solutionSizer.Add(wx.StaticText(self.p, label="Which word did you try?"), 0)
        solutionSizer.Add(self.WordDropDown, 1)
        solutionSizer.Add(wx.StaticText(self.p, label="\nHow many letters match?"), 0)
        solutionSizer.Add(self.LettersDropDown, 1)
        solutionSizer.Add(goButton, 1, wx.ALIGN_RIGHT)
        solutionSizer.Add(self.SolutionLabel, 0)
        

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wordsSizer, 1)
        sizer.Add(solutionSizer, 1)
        
        self.p.SetSizerAndFit(sizer)
        self.p.SetAutoLayout(1)
        sizer.Fit(self.p)
        self.Fit()
        self.Center()

##        self.SetSolutionPanel()

    def OnAddWord(self, event):
        print self.wordlist
        word = str(self.AddWordBox.GetValue()).upper()
        if (not word in self.wordlist.keys() and 
            (not self.wordlist or len(self.wordlist.keys()[0]) == len(word))
            ):
            self.WordsBox.Append(word)
            self.wordlist[word] = 0
            self.SetSolutionPanel()
            self.AddWordBox.SetValue('')
        
        self.AddWordBox.SetFocus()
        self.AddWordBox.SetSelection(0,99)

    def SetSolutionPanel(self):
        self.WordDropDown.SetItems(sorted(self.WordsBox.GetItems()))
        self.weight_wordlist()
        print self.wordlist
        best_word = self.get_best_word()
        print best_word
        if best_word:
            index = self.WordDropDown.GetItems().index(best_word)
            self.WordDropDown.SetSelection(index)
            nums = [str(i) for i in range(len(best_word)+1)]
            self.LettersDropDown.SetItems(nums)
        else:
            self.WordDropDown.SetSelection(0)
        self.LettersDropDown.SetSelection(0)
        self.SolutionLabel.SetLabel(self.SolutionText.format(best_word))
        self.AddWordBox.SetFocus()
        self.AddWordBox.SelectAll()

    def OnDeleteWord(self, event):
        if self.WordsBox.GetSelection():
            self.WordsBox.Delete(self.WordsBox.GetSelection())
            del self.wordlist[self.WordsBox.GetSelection()]
            self.SetSolutionPanel()

    def OnGuessWord(self, event):
        self.prune_list(str(self.WordDropDown.GetString(self.WordDropDown.GetSelection())),
                        int(self.LettersDropDown.GetString(self.LettersDropDown.GetSelection())))
        self.WordsBox.Set(self.wordlist.keys())
        self.SetSolutionPanel()

    def OnClear(self, event):
        self.WordsBox.Clear()
        self.wordlist = {}

    def OnGainFocusTB(self, event):
        wx.CallAfter(event.GetEventObject().SelectAll)
        event.Skip()
    
    def OnExit(self, event):
        pass
        
    def compare_letters(self, word1, word2):
        if len(word1) != len(word2):
            return -1
        i = 0
        for index in range(len(word1)):
            if word1[index]==word2[index]:
                i += 1
        return i

    def weight_wordlist(self): 
         for a in self.wordlist.keys(): 
             tlist = [] 
             for b in self.wordlist.keys(): 
                 if a != b: 
                     t = self.compare_letters(a,b) 
                     if t not in tlist: 
                         tlist.append(t) 
             self.wordlist[a] = len(tlist)

    def best_word_sort(self, w1, w2):
        return self.wordlist[w1] - self.wordlist[w2]

    def get_best_word(self): 
         if not self.wordlist: 
             return "" 
         return sorted(self.wordlist.keys(), cmp=self.best_word_sort)[-1]

    def prune_list(self, w, letters): 
         word = w.upper() 
         del(self.wordlist[word]) 
         for k in self.wordlist.keys(): 
             if self.compare_letters(word,k) != letters: 
                 del(self.wordlist[k])
    
    def about(self):
        tkMessageBox.showinfo(
            "Fallout PW Hacker v%s" % (VERSION),
            "(c) 2015 Marco262\nLast Updated: %s" % (LAST_UPDATED)
        )

def exit_root():
    root.destroy()
    root.quit()

if __name__ == "__main__":
    app = wx.App(redirect=False)
    MyFrame(title="Fallout PW Hacker v{0}".format(VERSION)).Show()
    app.MainLoop()
