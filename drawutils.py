import ROOT

leg_positions = {
    "left": {
        "xmin": 0.15,
        "xmax": 0.57,
        "ymin": 0.80,
        "ymax": 0.93,
    },
    "right": {
        "xmin": 0.51,
        "xmax": 0.93,
        "ymin": 0.80,
        "ymax": 0.93,
    },
    "top": {
        "xmin": 0.15,
        "xmax": 0.57,
        "ymin": 0.80,
        "ymax": 0.93,
    },
}
leg_positions_ratio = {
    "left": {
        "xmin": 0.15,
        "xmax": 0.59,
        "ymin": 0.74,
        "ymax": 0.90,
    },
    "right": {
        "xmin": 0.50,
        "xmax": 0.94,
        "ymin": 0.74,
        "ymax": 0.90,
    },
    "top": {
        "xmin": 0.15,
        "xmax": 0.59,
        "ymin": 0.74,
        "ymax": 0.90,
    },
}


#===================================================================================================
colourdict = {
    'orange':      '#E24A33',
    'purple':      '#7A68A6',
    'blue':        '#348ABD',
    'lblue':       '#68add5',
    'turquoise':   '#188487',
    'red':         '#A60628',
    'pink':        '#CF4457',
    'green':       '#32b43c',
    'lgreen':      '#88de8f',
    'yellow':      '#e2a233',
    'lyellow':     '#f7fab3',
    'grey':        '#838283',
    'gray':        '#838283',
}
#===================================================================================================

#===================================================================================================
def get_color(c):
    """Get ROOT color from name or HEX code

    Args:
        c (str): Name of the color, or HEX code, or ROOT color code

    Returns:
        TColor: ROOT colour
    """
    if not isinstance(c, str):
        return c

    if c.startswith('#'):
        colour = ROOT.TColor.GetColor(c)
    else:
        try:
            colour = ROOT.TColor.GetColor(colourdict[c])
        except KeyError:
            if '+' in c:
                col, n = c.split('+')
                colour = getattr(ROOT, col)
                colour += int(n)
            elif '-' in c:
                col, n = c.split('-')
                colour = getattr(ROOT, col)
                colour -= int(n)
            else:
                colour = getattr(ROOT, c)

    return colour
#===================================================================================================

#===================================================================================================
def set_color(obj, color, fill=False, alpha=None):
    """Set color to object

    Args:
        obj (*): Object to apply color
        color (str): Name of color
        fill (bool, optional): whether to set the filling color or not. Defaults to False.
        alpha (float, optional): transparency value for filling. Defaults to None.
    """
    color = get_color(color)
    obj.SetLineColor(color)
    obj.SetMarkerColor(color)
    if fill:
        if alpha is not None:
            obj.SetFillColorAlpha(color, alpha)
        else:
            obj.SetFillColor(color)
    return
#===================================================================================================

#===================================================================================================
def set_style(obj, **kwargs):
    """Set style attributes to object

    Args:
        obj (*): object to which the style attributes are applied
    """

    # check if hist or graph
    is_hist = obj.InheritsFrom('TH1')

    color = kwargs.get('color', ROOT.kBlack)
    alpha = kwargs.get('alpha', None)

    mstyle = kwargs.get('mstyle', 20)   # marker style
    fstyle = kwargs.get('fstyle', None) # fill style
    lstyle = kwargs.get('lstyle',None)  # line style

    msize  = kwargs.get('msize', 0.8)  # marker size
    lwidth = kwargs.get('lwidth', 2)   # line width

    fill = (kwargs.get('fill', False) or fstyle is not None)

    xtitle = kwargs.get('xtitle', None)
    ytitle = kwargs.get('ytitle', None)

    xmin = kwargs.get('xmin', None)
    xmax = kwargs.get('xmax', None)
    ymin = kwargs.get('ymin', None)
    ymax = kwargs.get('ymax', None)

    # default
    obj.SetTitle('')
    if is_hist:
        obj.SetStats(0)

    # color
    set_color(obj, color, fill, alpha)

    # marker
    obj.SetMarkerStyle(mstyle)
    obj.SetMarkerSize(msize)

    # line
    obj.SetLineWidth(lwidth)
    if lstyle is not None:
        obj.SetLineStyle(lstyle)

    # fill
    if fstyle is not None:
        obj.SetFillStyle(fstyle)

    # axis titles
    if xtitle is not None:
        obj.GetXaxis().SetTitle(xtitle)
    if ytitle is not None:
        obj.GetYaxis().SetTitle(ytitle)

    if xmin is not None and xmax is not None:
        obj.GetXaxis().SetRangeUser(xmin, xmax)
    if ymin is not None and ymax is not None:
        obj.GetYaxis().SetRangeUser(ymin, ymax)
    return
#===================================================================================================

#===================================================================================================
def format_canvas(ratio, name='', title='', width=800, height=800, logy=False, logx=False, **kwargs):
    
    lmargin_c = kwargs.get('lmargin_c', 0.13)
    rmargin_c = kwargs.get('rmargin_c', 0.03)
    bmargin_c = kwargs.get('bmargin_c', 0.13)
    tmargin_c = kwargs.get('tmargin_c', 0.05)
    
    if ratio:
        # upper pad in case of ratio
        lmargin_u = kwargs.get('lmargin_u', lmargin_c)
        rmargin_u = kwargs.get('rmargin_u', rmargin_c)
        bmargin_u = kwargs.get('bmargin_u', 0.005)
        tmargin_u = kwargs.get('tmargin_u', 0.08)
        # lower pad in case of ratio
        lmargin_d = kwargs.get('lmargin_d', lmargin_c)
        rmargin_d = kwargs.get('rmargin_d', rmargin_c)
        bmargin_d = kwargs.get('bmargin_d', 0.35)
        tmargin_d = kwargs.get('tmargin_d', 0.0054)
    
    can = ROOT.TCanvas(name, title, width, height)
    can.SetTicks(1,1)
    can.SetLeftMargin  (lmargin_c)
    can.SetTopMargin   (tmargin_c)
    can.SetRightMargin (rmargin_c)
    can.SetBottomMargin(bmargin_c)
    
    if ratio:
        cup   = ROOT.TPad("u", "u", 0., 0.305, 0.99, 1)
        cdown = ROOT.TPad("d", "d", 0., 0.01 , 0.99, 0.295)
        
        cup.SetTicks  (1, 1)
        cdown.SetTicks(1, 1)

        cup.SetLeftMargin  (lmargin_u)
        cup.SetRightMargin (rmargin_u)
        cup.SetBottomMargin(bmargin_u)
        cup.SetTopMargin   (tmargin_u)

        cdown.SetTicks(1, 1)
        cdown.SetLeftMargin  (lmargin_d)
        cdown.SetRightMargin (rmargin_d)
        cdown.SetBottomMargin(bmargin_d)
        cdown.SetTopMargin   (tmargin_d)
        
        if logy:
            cup.SetLogy()
        if logx:
            cup.SetLogx()
            cdown.SetLogx()
        
        cup.Draw()
        cdown.Draw()
        return can, cup, cdown
    else:
        if logy:
            can.SetLogy()
        if logx:
            can.SetLogx()
        return can
#===================================================================================================

#===================================================================================================
def format_upper_pad_axis(ratio=True, xlabel=None, ylabel=None, xrange=None, yrange=None,
                          ax=None, ay=None, logy=False, ydivisions=None, xdivisions=None, hist=None,
                          **kwargs):
    
    y_titleoffset = kwargs.get('y_titleoffset', 1.8  if not ratio else 1.1)
    x_titleoffset = kwargs.get('x_titleoffset', 1.2  if not ratio else 1.2)
    y_titlesize   = kwargs.get('y_titlesize'  , 0.04 if not ratio else 0.05)
    y_labelsize   = kwargs.get('y_labelsize'  , 0.04 if not ratio else 0.05)
    x_titlesize   = kwargs.get('x_titlesize'  , 0.04 if not ratio else 0)
    x_labelsize   = kwargs.get('x_labelsize'  , 0.04 if not ratio else 0)
    
    if ay:
        if yrange:
            if logy and yrange[0]==0: y_min = 1.
            else: y_min = yrange[0]
            if hist:
                if hist.InheritsFrom('THStack') or hist.InheritsFrom('RooPrintable'):
                    hist.SetMinimum(y_min)
                    hist.SetMaximum(yrange[1])
            else:
                ay.SetRangeUser(y_min, yrange[1])
            
        if ylabel    : ay.SetTitle(ylabel)
        ay.SetTitleOffset(y_titleoffset)
        ay.SetTitleSize(y_titlesize)
        ay.SetLabelSize(y_labelsize)
        if ydivisions: ay.SetNdivisions(ydivisions)
    if ax:
        if xrange:
            ax.SetRangeUser(xrange[0], xrange[1])
        if xlabel: ax.SetTitle(xlabel)
        ax.SetLabelSize(x_labelsize)
        ax.SetTitleOffset(x_titleoffset)
        ax.SetTitleSize(x_titlesize)
        if xdivisions: ax.SetNdivisions(xdivisions)
    return
#===================================================================================================

#===================================================================================================
def format_lower_pad_axis(ratio=True, xlabel=None, ylabel=None, xrange=None, yrange=None,
                          ax=None, ay=None, **kwargs):
    
    if not yrange: yrange = [0.3, 1.7]
    y_titleoffset = kwargs.get('y_titleoffset', 0.4)
    x_titleoffset = kwargs.get('x_titleoffset', 1.10)
    y_labeloffset = kwargs.get('y_labeloffset', 0.015)
    x_labeloffset = kwargs.get('x_labeloffset', 0.0)
    y_ticklength  = kwargs.get('y_ticklength' , None)
    x_ticklength  = kwargs.get('x_ticklength' , 0.06)
    y_titlesize   = kwargs.get('y_titlesize'  , 0.12)
    y_labelsize   = kwargs.get('y_labelsize'  , 0.12)
    x_titlesize   = kwargs.get('x_titlesize'  , 0.12)
    x_labelsize   = kwargs.get('x_labelsize'  , 0.14)
    xdivisions    = kwargs.get('xdivisions'   , 203)
    ydivisions    = kwargs.get('ydivisions'   , 504)

    if ay:
        ay.SetRangeUser(yrange[0], yrange[1])
        if ratio:  ay.SetNdivisions(ydivisions)
        if ylabel: ay.SetTitle(ylabel)

        ay.CenterTitle()
        
        if y_ticklength: ay.SetTickLength(y_ticklength)
        
        ay.SetTitleOffset(y_titleoffset)
        ay.SetTitleSize(y_titlesize)
        ay.SetLabelSize(y_labelsize)
        ay.SetLabelOffset(y_labeloffset)

    if ax:
        if xrange: ax.SetRangeUser(xrange[0], xrange[1])
        if xlabel: ax.SetTitle(xlabel)
        
        ax.SetNdivisions(xdivisions)
        
        if x_ticklength: ax.SetTickLength(x_ticklength)
        
        ax.SetTitleOffset(x_titleoffset)
        ax.SetTitleSize(x_titlesize)
        ax.SetLabelSize(x_labelsize)
        ax.SetLabelOffset(x_labeloffset)
    return
#===================================================================================================

#===================================================================================================
def get_yrange(hists, get_min=False, get_max=False, lim_value=None):
    if get_max:
        maxs = []
        try:
            for h in hists:
                if lim_value is not None:
                    maxs.append(h.GetMaximum(lim_value))
                else:
                    maxs.append(h.GetMaximum())
        except:
            for h in hists.values():
                if lim_value is not None:
                    maxs.append(h.GetMaximum(lim_value))
                else:
                    maxs.append(h.GetMaximum())
        maximum = max(maxs)
        return maximum
    if get_min:
        mins = []
        try:
            for h in hists:
                if lim_value is not None:
                    mins.append(h.GetMinimum(lim_value))
                else:
                    mins.append(h.GetMinimum())
        except:
            for h in hists.values():
                if lim_value is not None:
                    mins.append(h.GetMinimum(lim_value))
                else:
                    mins.append(h.GetMinimum())
        minimum = min(mins)
        return minimum
#===================================================================================================

#===================================================================================================
def format_legend(size=0.035, legpos=None, xmin=0.50, xmax=0.9, ymin=0.7, ymax=0.9, ratio=False, ncols=1):
    if legpos:
        legend_positions = leg_positions_ratio if ratio else leg_positions
        xmin, xmax, ymin, ymax = (val for val in legend_positions[legpos].values())
    leg = ROOT.TLegend(xmin, ymin, xmax, ymax)
    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetTextSize(size)
    leg.SetEntrySeparation(size/3.0)
    leg.SetFillColorAlpha(0, 0)
    if ncols > 1:
        leg.SetNColumns(ncols)
    return leg
#===================================================================================================

#===================================================================================================
def latex_label(size, x, y, msg):
    lat = ROOT.TLatex()
    lat.SetTextFont(42)
    lat.SetTextSize(size)
    lat.DrawLatexNDC(x, y, msg)
    return
#===================================================================================================

#===================================================================================================
def atlas_label(x=None, y=None, size=0.04, msg="Internal", ndc=True):
    lat = ROOT.TLatex()
    lat.SetTextFont(42)
    lat.SetTextSize(size)
    if ndc:
        lat.DrawLatexNDC(x, y, "#bf{#it{ATLAS}} "+msg)
    else:
        lat.DrawLatex(x, y, "#bf{#it{ATLAS}} "+msg)
    return
#===================================================================================================