import ROOT
from seaborn import color_palette

leg_positions = {
    "left": {
        "xmin": 0.15,
        "xmax": 0.57,
        "ymin": 0.76,
        "ymax": 0.93,
    },
    "right": {
        "xmin": 0.51,
        "xmax": 0.93,
        "ymin": 0.76,
        "ymax": 0.93,
    },
    "top": {
        "xmin": 0.15,
        "xmax": 0.57,
        "ymin": 0.76,
        "ymax": 0.93,
    },
}
leg_positions_ratio = {
    "left": {
        "xmin": 0.15,
        "xmax": 0.59,
        "ymin": 0.74,
        "ymax": 0.86,
    },
    "right": {
        "xmin": 0.50,
        "xmax": 0.94,
        "ymin": 0.74,
        "ymax": 0.86,
    },
    "top": {
        "xmin": 0.15,
        "xmax": 0.59,
        "ymin": 0.74,
        "ymax": 0.86,
    },
}


#===================================================================================================
colourdict = {
    'black':       '#000000',
    'blue':        '#348ABD',
    'red':         '#A60628',
    'orange':      '#E24A33',
    'purple':      '#7A68A6',
    'lblue':       '#68add5',
    'turquoise':   '#188487',
    'pink':        '#CF4457',
    'green':       '#32b43c',
    'yellow':      '#e2a233',
    'grey':        '#838283',
    'lgreen':      '#88de8f',
    'lyellow':     '#f7fab3',
}
#===================================================================================================

#===================================================================================================
def get_colors_seaborn(number_colors, iel):
    colors = color_palette('muted', number_colors)
    return colors.as_hex()[iel]
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
def format_canvas(pads2, name='', title='', logy=False, logx=False, **kwargs):
    
    width       = kwargs.get('width', 800)
    height      = kwargs.get('height', 800)
    second_axis = kwargs.get('second_axis', False)
    lmargin_c   = kwargs.get('lmargin_c', 0.13)
    bmargin_c   = kwargs.get('bmargin_c', 0.13)
    tmargin_c   = kwargs.get('tmargin_c', 0.05)
    
    if second_axis:
        rmargin_c   = kwargs.get('rmargin_c', 0.07)
    else:
        rmargin_c   = kwargs.get('rmargin_c', 0.03)
    
    if pads2:
        xmin_u = kwargs.get('xmin_u', 0.)
        xmax_u = kwargs.get('xmax_u', 0.99)
        xmin_d = kwargs.get('xmin_d', 0.)
        xmax_d = kwargs.get('xmax_d', 0.99)
        
        ymin_u = kwargs.get('ymin_u', 0.305)
        ymax_u = kwargs.get('ymax_u', 1.0)
        ymin_d = kwargs.get('ymin_d', 0.01)
        ymax_d = kwargs.get('ymax_d', 0.295)
        
        # upper pad in case of ratio
        lmargin_u = kwargs.get('lmargin_u', lmargin_c)
        rmargin_u = kwargs.get('rmargin_u', rmargin_c)
        bmargin_u = kwargs.get('bmargin_u', 0.017)
        tmargin_u = kwargs.get('tmargin_u', 0.08)
        # lower pad in case of ratio
        lmargin_d = kwargs.get('lmargin_d', lmargin_c)
        rmargin_d = kwargs.get('rmargin_d', rmargin_c)
        bmargin_d = kwargs.get('bmargin_d', 0.35)
        tmargin_d = kwargs.get('tmargin_d', 0.02)
        
        
    can = ROOT.TCanvas(name, title, width, height)
    can.SetTicks(1,1)
    can.SetLeftMargin  (lmargin_c)
    can.SetTopMargin   (tmargin_c)
    can.SetRightMargin (rmargin_c)
    can.SetBottomMargin(bmargin_c)
    
    if pads2:
        cup   = ROOT.TPad("u", "u", xmin_u, ymin_u, xmax_u, ymax_u)
        cdown = ROOT.TPad("d", "d", xmin_d, ymin_d, xmax_d, ymax_d)
        
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
def format_upper_pad_axis(pad, pads2, xlabel=None, ylabel=None, xrange=None, yrange=None,
                          ax=None, ay=None, logy=False, logx=False, ydivisions=510, xdivisions=None, hist=None,
                          **kwargs):
    
    txtsize = calc_size(pad)*0.9
    y_titleoffset  = kwargs.get('y_titleoffset' , 1.1 if pads2 else 1.8)
    x_titleoffset  = kwargs.get('x_titleoffset' , 1.2)
    y_titlesize    = kwargs.get('y_titlesize'   , txtsize)
    y_labelsize    = kwargs.get('y_labelsize'   , txtsize)
    x_titlesize    = kwargs.get('x_titlesize'   , txtsize if not pads2 else 0)
    x_labelsize    = kwargs.get('x_labelsize'   , txtsize if not pads2 else 0)
    y_centertitle  = kwargs.get('y_centertitle' , False)
    # sec_axis       = kwargs.get('sec_axis'      , None) # when it is not none, its a histogram/tgraph
    # sec_axis_label = kwargs.get('sec_axis_label', None) # when it is not none, its a histogram/tgraph
    
    if ay:
        if yrange:
            if logy and yrange[0]==0: y_min = 1.
            else: y_min = yrange[0]
            if hist:
                if hist.InheritsFrom('THStack') or hist.InheritsFrom('RooPrintable') or hist.InheritsFrom('TGraph'):
                    hist.SetMinimum(y_min)
                    hist.SetMaximum(yrange[1])
                else:
                    ay.SetRangeUser(y_min, yrange[1])
            else:
                ay.SetRangeUser(y_min, yrange[1])
        
        if y_centertitle: ay.CenterTitle()
        
        # if sec_axis:
        #     pad.SetTicks(1, 0)
        #     format_second_axis(sec_axis, yrange, sec_axis_label)
 
        if ylabel    : ay.SetTitle(ylabel)
        ay.SetTitleOffset(y_titleoffset)
        ay.SetTitleSize(y_titlesize)
        ay.SetLabelSize(y_labelsize)
        if ydivisions: ay.SetNdivisions(ydivisions)
    if ax:
        if logx: ax.SetMoreLogLabels()
        if xrange:
            if logx and xrange[0]==0:
                if xrange[1]<=1:
                    x_min = 1e-5
                else:            x_min = 1.
            else: x_min = xrange[0]
            ax.SetRangeUser(x_min, xrange[1])
        else:
            if logx and ax.GetXmin()==0.:
                if ax.GetXmax()<=1: x_min = 0.000001
                else:               x_min = 1.
            else: x_min = ax.GetXmin()
            
            ax.SetRange(1, ax.GetNbins())
        if xlabel: ax.SetTitle(xlabel)
        ax.SetLabelSize(x_labelsize)
        ax.SetTitleOffset(x_titleoffset)
        ax.SetTitleSize(x_titlesize)
        if xdivisions: ax.SetNdivisions(xdivisions)
    return txtsize
#===================================================================================================

#===================================================================================================
def format_lower_pad_axis(pad, xlabel=None, ylabel=None, xrange=None, yrange=None, logx=False,
                          ax=None, ay=None, **kwargs):
    
    txtsize = calc_size(pad)*0.9
    if not yrange: yrange = [0.3, 1.7]
    y_titleoffset  = kwargs.get('y_titleoffset', 0.4)
    x_titleoffset  = kwargs.get('x_titleoffset', 1.18)
    y_labeloffset  = kwargs.get('y_labeloffset', None)
    x_labeloffset  = kwargs.get('x_labeloffset', None)
    y_ticklength   = kwargs.get('y_ticklength' , None)
    x_ticklength   = kwargs.get('x_ticklength' , None)
    y_titlesize    = kwargs.get('y_titlesize'  , txtsize)
    y_labelsize    = kwargs.get('y_labelsize'  , txtsize)
    x_titlesize    = kwargs.get('x_titlesize'  , txtsize)
    x_labelsize    = kwargs.get('x_labelsize'  , txtsize)
    xdivisions     = kwargs.get('xdivisions'   , None)
    ydivisions     = kwargs.get('ydivisions'   , None)
    sec_axis       = kwargs.get('sec_axis'     , None)
    hist           = kwargs.get('hist'         , None)
    gridx          = kwargs.get('gridx'        , False)
    gridy          = kwargs.get('gridy'        , False)

    if gridx:
        pad.SetGridx()
    if gridy:
        pad.SetGridy()

    if ay:
        if hist:
            if hist.Class() == 'TH1D' or hist.Class() == 'TH1F' or hist.Class() == 'TH1':
                ay.SetRangeUser(yrange[0], yrange[1])
            elif hist.InheritsFrom('THStack') or hist.InheritsFrom('RooPrintable') or hist.InheritsFrom('TGraph'):
                hist.SetMinimum(yrange[0])
                hist.SetMaximum(yrange[1])
        else:
            ay.SetRangeUser(yrange[0], yrange[1])
        # ay.SetRangeUser(yrange[0], yrange[1])
        if ydivisions: ay.SetNdivisions(ydivisions)
        if ylabel    : ay.SetTitle(ylabel)

        ay.CenterTitle()
        
        if sec_axis:
            pad.SetTicks(1, 0)
        
        if y_ticklength: ay.SetTickLength(y_ticklength)
        
        ay.SetTitleOffset(y_titleoffset)
        ay.SetTitleSize(y_titlesize)
        ay.SetLabelSize(y_labelsize)
        if y_labeloffset: ay.SetLabelOffset(y_labeloffset)


    if ax:
        if logx: ax.SetMoreLogLabels()
        if xrange:    
            if logx and xrange[0]==0: x_min = 1.
            else: x_min = xrange[0]
            if hist and hist.InheritsFrom('TGraph'):
                ax.SetLimits(x_min, xrange[1])
            else:
                ax.SetRangeUser(x_min, xrange[1])
        if xlabel: ax.SetTitle(xlabel)
        
        if xdivisions: ax.SetNdivisions(xdivisions)
        
        if x_ticklength: ax.SetTickLength(x_ticklength)
        
        ax.SetTitleOffset(x_titleoffset)
        ax.SetTitleSize(x_titlesize)
        ax.SetLabelSize(x_labelsize)
        if x_labeloffset: ax.SetLabelOffset(x_labeloffset)
    return txtsize
#===================================================================================================

#===================================================================================================
def format_canvas_2d(canv_name="", logx=False, logy=False, logz=False, **kwargs):

    width   = kwargs.get('width' , 800)
    height  = kwargs.get('height', 800)
    lmargin = kwargs.get('lmargin', 0.12)
    rmargin = kwargs.get('rmargin', 0.18)
    tmargin = kwargs.get('tmargin', 0.08)
    bmargin = kwargs.get('bmargin', 0.12)

    can = ROOT.TCanvas(canv_name, "", width, height)
    can.SetTicks(1,1)

    can.SetLeftMargin  (lmargin)
    can.SetRightMargin (rmargin)
    can.SetBottomMargin(bmargin)
    can.SetTopMargin   (tmargin)

    if logy: can.SetLogy()
    if logx: can.SetLogx()
    if logz: can.SetLogz()

    return can
#===================================================================================================

#===================================================================================================
def format_axis_2d(ax=None, ay=None, az=None, xlabel=None, ylabel=None, zlabel=None, xrange=None,
                   yrange=None, zrange=None, **kwargs):
    
    y_titleoffset = kwargs.get('y_titleoffset', 1.2 )
    y_titlesize   = kwargs.get('y_titlesize'  , 0.04)
    y_labelsize   = kwargs.get('y_labelsize'  , 0.03)
    x_titleoffset = kwargs.get('x_titleoffset', 1.0 )
    x_titlesize   = kwargs.get('x_titlesize'  , 0.04)
    x_labelsize   = kwargs.get('x_labelsize'  , 0.03)

    z_titlesize   = kwargs.get('z_titlesize'  , 0.04)
    z_labelsize   = kwargs.get('z_labelsize'  , 0.03)
    z_titleoffset = kwargs.get('z_titleoffset', 1.5)
    
    
    if ay:
        ay.SetLabelSize  (y_labelsize)
        ay.SetTitleOffset(y_titleoffset)
        ay.SetTitleSize  (y_titlesize)
        if ylabel:
            ay.SetTitle(ylabel)
        if yrange:
            ay.SetRangeUser(yrange[0], yrange[1])
        
    if ax:
        ax.SetLabelSize  (x_labelsize)
        ax.SetTitleOffset(x_titleoffset)
        ax.SetTitleSize  (x_titlesize)
        if xlabel:
            ax.SetTitle(xlabel)
        if xrange:
            ax.SetRangeUser(xrange[0], xrange[1])
    if az:
        az.SetLabelSize(z_labelsize)
        az.SetTitleSize(z_titlesize)
        az.SetTitleOffset(z_titleoffset)
        if zlabel:
            az.SetTitle(zlabel)
        if zrange:
            az.SetRangeUser(zrange[0], zrange[1])
    
    return
#===================================================================================================

#===================================================================================================
def format_second_axis(pad, ax, yrange, axisrange, label, **kwargs):
    
    txtsize = calc_size(pad)*0.9
    y_titleoffset  = kwargs.get('y_titleoffset', 0.4)
    y_labeloffset  = kwargs.get('y_labeloffset', None)
    y_ticklength   = kwargs.get('y_ticklength' , None)
    y_titlesize    = kwargs.get('y_titlesize'  , txtsize)
    y_labelsize    = kwargs.get('y_labelsize'  , txtsize)
    
    x_pos       = ax.GetXmax()
    second_axis = ROOT.TGaxis(x_pos, yrange[0],
                              x_pos, yrange[1],
                              axisrange[0], axisrange[1], 510, "+L")
    second_axis.SetLineColor(ROOT.kRed)
    second_axis.SetLabelColor(ROOT.kRed)
    second_axis.SetTitleColor(ROOT.kRed)
    second_axis.SetTitleOffset(y_titleoffset)
    second_axis.SetTitleSize(y_titlesize)
    second_axis.SetLabelSize(y_labelsize)
    if y_ticklength: second_axis.SetTickLength(y_ticklength)
    if y_labeloffset: second_axis.SetLabelOffset(y_labeloffset)
    second_axis.SetTitle(label)
    return second_axis
#===================================================================================================

#===================================================================================================
def get_yrange(hists, get_min=False, get_max=False, lim_value=None, werror=False):
    if lim_value is None:
        lim_value = float('inf')
        if get_min: lim_value = -lim_value

    if not (isinstance(hists, list) or isinstance(hists, dict)):
        hists = [hists, ]

    def _getmin(h):
        if werror:
            _mins = []
            for b in range(1, h.GetNbinsX()+1):
                cont = h.GetBinContent(b)
                err  = h.GetBinError(b)
                if cont-err > lim_value:
                    _mins.append(cont-err)
            _min = min(_mins)
            return _min
        else:
            return h.GetMinimum(lim_value)
    def _getmax(h):
        if werror:
            _maxs = []
            for b in range(1, h.GetNbinsX()+1):
                cont = h.GetBinContent(b)
                err  = h.GetBinError(b)
                if cont+err < lim_value:
                    _maxs.append(cont+err)
            _max = max(_maxs)
            return _max
        else:
            return h.GetMaximum(lim_value)

    def _get_maxmins(func, hs):
        elements = []
        try:
            for h in hs:
                elements.append(func(h))
        except:
            for h in hs.values():
                elements.append(func(h))
        return elements

    if get_max:
        return max(_get_maxmins(_getmax, hists))
    if get_min:
        mins = sorted(_get_maxmins(_getmin, hists))
        if lim_value == -float('inf'):
            return mins[0], mins[1]
        else:
            return mins[0]
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
def atlas_label(x, y, size=0.04, msg="Internal", ndc=True):
    lat = ROOT.TLatex()
    lat.SetTextFont(42)
    lat.SetTextSize(size)
    if ndc:
        lat.DrawLatexNDC(x, y, "#bf{#it{ATLAS}} "+msg)
    else:
        lat.DrawLatex(x, y, "#bf{#it{ATLAS}} "+msg)
    return
#===================================================================================================

#===================================================================================================
def lumi_label(x, y, lumi, comE, size=0.035, ndc=True):
    lat = ROOT.TLatex()
    lat.SetTextFont(42)
    lat.SetTextSize(size)
    
    if ndc:
        lat.DrawLatexNDC(x, y, '#sqrt{s} = %.1f TeV, %.1f fb^{-1}' % (comE, lumi))
    else:
        lat.DrawLatex(x, y, '#sqrt{s} = %.1f TeV, %.1f fb^{-1}' % (comE, lumi))
    return
#===================================================================================================

#===================================================================================================
def draw_ratio_lines(ratio, yvals, xmin=None, xmax=None):

    if not xmin and not xmax:
        firstbin = ratio.GetXaxis().GetFirst()
        lastbin  = ratio.GetXaxis().GetLast()
        xmax     = ratio.GetXaxis().GetBinUpEdge(lastbin)
        xmin     = ratio.GetXaxis().GetBinLowEdge(firstbin)

    lines = [None]*len(yvals)
    for i, y in enumerate(yvals):
        lines[i] = ROOT.TLine(xmin, y, xmax, y)
        ROOT.SetOwnership(lines[i], False)

    lines[0].SetLineWidth(1)
    lines[0].SetLineStyle(2)
    for line in lines[1:]:
        line.SetLineStyle(3)

    for line in lines:
        line.AppendPad()
        line.Draw()
    return
#===================================================================================================

#===================================================================================================
def draw_grid_lines(h):
    line = ROOT.TLine()
    line.SetLineColor(ROOT.kBlack)
    line.SetLineStyle(ROOT.kDashed)
    line.SetLineWidth(1)
    nbinsx = h.GetNbinsX()
    nbinsy = h.GetNbinsY()
    minx = h.GetXaxis().GetXmin()
    maxx = h.GetXaxis().GetXmax()
    miny = h.GetYaxis().GetXmin()
    maxy = h.GetYaxis().GetXmax()
    for ix in range(1, nbinsx):
        line.DrawLine(h.GetXaxis().GetBinUpEdge(ix), miny, h.GetXaxis().GetBinUpEdge(ix), maxy)
    for iy in range(1, nbinsy):
        line.DrawLine(minx, h.GetYaxis().GetBinUpEdge(iy), maxx, h.GetYaxis().GetBinUpEdge(iy))
    return
#===================================================================================================

#===================================================================================================
def set_default_style():
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetFrameFillColor(0)
    ROOT.gStyle.SetFrameBorderSize(0)
    ROOT.gStyle.SetFrameBorderMode(0)
    ROOT.gStyle.SetCanvasColor(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetTitleBorderSize(0)
    ROOT.gStyle.SetTitleFillColor(0)
    ROOT.gStyle.SetTextFont(132)
    ROOT.gStyle.SetLegendFont(132)
    ROOT.gStyle.SetLabelFont(132, "XYZ")
    ROOT.gStyle.SetTitleFont(132, "XYZ")
    ROOT.gStyle.SetEndErrorSize(0)
    ROOT.gStyle.SetPalette(71)
    return
#===================================================================================================

#===================================================================================================
def set_atlas_style():
    ROOT.gStyle.SetPalette(71)

    # use plain black on white colors
    icol = 0
    ROOT.gStyle.SetFrameBorderMode(icol)
    ROOT.gStyle.SetFrameFillColor(icol)
    ROOT.gStyle.SetCanvasBorderMode(icol)
    ROOT.gStyle.SetCanvasColor(icol)
    ROOT.gStyle.SetPadBorderMode(icol)
    ROOT.gStyle.SetPadColor(icol)
    ROOT.gStyle.SetStatColor(icol)

    # set the paper & margin sizes
    ROOT.gStyle.SetPaperSize(20,26)

    # set margin sizes
    ROOT.gStyle.SetPadTopMargin(0.05)
    ROOT.gStyle.SetPadRightMargin(0.05)
    ROOT.gStyle.SetPadBottomMargin(0.16)
    ROOT.gStyle.SetPadLeftMargin(0.16)

    # set title offsets (for axis label)
    ROOT.gStyle.SetTitleXOffset(1.4)
    ROOT.gStyle.SetTitleYOffset(1.4)

    # use large fonts
    font = 42 # Helvetica
    tsize = 0.05
    ROOT.gStyle.SetTextFont(font)
    ROOT.gStyle.SetTextSize(tsize)

    ROOT.gStyle.SetLabelFont(font, "x")
    ROOT.gStyle.SetTitleFont(font, "x")
    ROOT.gStyle.SetLabelFont(font, "y")
    ROOT.gStyle.SetTitleFont(font, "y")
    ROOT.gStyle.SetLabelFont(font, "z")
    ROOT.gStyle.SetTitleFont(font, "z")

    ROOT.gStyle.SetLabelSize(tsize, "x")
    ROOT.gStyle.SetTitleSize(tsize, "x")
    ROOT.gStyle.SetLabelSize(tsize, "y")
    ROOT.gStyle.SetTitleSize(tsize, "y")
    ROOT.gStyle.SetLabelSize(tsize, "z")
    ROOT.gStyle.SetTitleSize(tsize, "z")

    # use bold lines and markers
    ROOT.gStyle.SetMarkerStyle(20)
    ROOT.gStyle.SetMarkerSize(1.2)
    ROOT.gStyle.SetHistLineWidth(2)
    ROOT.gStyle.SetLineStyleString(2, "[12 12]")
    ROOT.gStyle.SetEndErrorSize(0.)

    # do not display any of the standard histogram decorations
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptFit(0)
    return
#===================================================================================================

#===================================================================================================
def calc_size(pad):
        pad_width  = pad.XtoPixel(pad.GetX2())
        pad_height = pad.YtoPixel(pad.GetY1())

        if pad_width < pad_height:
            tsize = 28.6 / pad_width
        else:
            tsize = 28.6 / pad_height
        return tsize
#===================================================================================================

#===================================================================================================
def draw_fitresult(xmin, xmax, ymin, ymax, props, size=0.02):
    
    pave = ROOT.TPaveText(xmin, ymin, xmax, ymax, "NDC NB")
    pave.SetFillColorAlpha(ROOT.kWhite, 0.0)
    pave.SetLineColorAlpha(ROOT.kWhite, 0.0)
    pave.SetTextFont(42)
    pave.SetTextColor(ROOT.kBlack)
    pave.SetTextSize(size)
    pave.SetTextAlign(11)
    
    if isinstance(props, dict):
        lines = []
        
        if 'ndof' in props:
            lines.append('{:11s} = {:.2f} / {} = {:.3f}'.format('Chi2 / NDF', props['chi2'], props['ndof'], props['chi2_o_ndof']))
            lines.append('{:11s} = {}'.format('p-value', props['pvalue']))
        else:
            lines.append('{:11s} = {:.2f}'.format('Chi2', props['chi2']))

        if 'nsig' in props and props['nsig'] is not None:
            try:
                lines.append('{:11s} = {:.4f} #pm {:.5f},   N_{{sig}}/#sigma_{{N_{{sig}}}} = {}'.format('N_{sig}', props['nsig'], props['nsigerr'], props['nsig']/props['nsigerr']))
            except ZeroDivisionError:
                lines.append('{:11s} = {:.4f} #pm {:.5f},   N_{{sig}}/#sigma_{{N_{{sig}}}} = {}'.format('N_{sig}', props['nsig'], props['nsigerr'], 0.))
        if 'nbkg' in props and props['nbkg'] is not None:
            lines.append('{:11s} = {:.4f} #pm {:.5f}'.format('N_{bkg}', props['nbkg'], props['nbkgerr']))


        for propname, prop in props.items():
            if propname == 'variables':
                for ivar in range(prop.getSize()):
                    par = prop.at(ivar)
                    parname = par.getTitle().Data()
                    parvalue = par.getVal()
                    parerror = par.getError()

                    if parerror < 0.01:
                        precision = 4
                    else:
                        precision = 2
                    this_line = f'{parname:10} = {parvalue:.{precision}f} +/- {parerror:.{precision}f}'
                    lines.append(this_line)
            

        for this_line in lines:
            pave.AddText(this_line)
    
    elif props.InheritsFrom('TF1'):
        chi2 = props.GetChisquare()
        ndf  = props.GetNDF()
        lines = []
        lines.append('{:11s} = {:.2f} / {}'.format('Chi2 / NDF', chi2, ndf))
        for ipar in range(props.GetNpar()):
            parname  = props.GetParName(ipar)
            parvalue = props.GetParameter(ipar)
            parerror = props.GetParError(ipar)
            if parvalue < 0.01:
                precision = 4
            else:
                precision = 2            
            this_line = f'{parname:10} = {parvalue:.{precision}f} +/- {parerror:.{precision}f}'
            lines.append(this_line)
        
        for this_line in lines:
            pave.AddText(this_line)
   
    
    return pave
#===================================================================================================
